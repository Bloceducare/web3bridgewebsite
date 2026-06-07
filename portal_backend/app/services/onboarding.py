import asyncio
import logging
import re
from datetime import UTC, date, datetime
from urllib.parse import urlencode

from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.portal import (
    AccountState,
    ApprovalStatus,
    AuditLog,
    ExternalStudentMap,
    OnboardingStatus,
    StudentProfile,
    StudentStatusHistory,
    User,
    UserRole,
)
from app.schemas.onboarding import OnboardingInviteRequest, OnboardingInviteResponse
from app.services.auth import AuthService
from app.services.email import EmailService
from app.services.status_mapping import normalize_approval_status

settings = get_settings()
logger = logging.getLogger(__name__)


class OnboardingService:
    def __init__(
        self,
        session: AsyncSession,
        *,
        email_service: EmailService | None = None,
    ) -> None:
        self.session = session
        self.auth_service = AuthService(session)
        self.email_service = email_service or EmailService()

    @staticmethod
    def is_zk_course(course_name: str) -> bool:
        name = course_name.lower().strip()
        return bool(re.search(r"\bzk\b|zero[- ]?knowledge", name))

    @staticmethod
    def build_activation_url(token: str) -> str:
        query = urlencode({"token": token})
        return f"{settings.PORTAL_FRONTEND_URL.rstrip('/')}/activate/onboard?{query}"

    @staticmethod
    def should_issue_activation_invite(
        *,
        portal_invite_created: bool,
        account_state: str,
        onboarding_status: str | None = None,
    ) -> bool:
        if portal_invite_created:
            return True
        if account_state == AccountState.INVITED.value:
            return True
        if (onboarding_status or "") in (
            OnboardingStatus.PENDING.value,
            OnboardingStatus.INVITED.value,
        ):
            return account_state not in (
                AccountState.ACTIVE.value,
                AccountState.SUSPENDED.value,
                AccountState.DEACTIVATED.value,
            )
        return False

    @staticmethod
    def resolve_invite_reason(
        *,
        portal_invite_created: bool,
        account_state: str,
        issued_invite: bool,
    ) -> str:
        if portal_invite_created:
            return "portal_invite_created"
        if issued_invite:
            return "portal_invite_resent"
        if account_state == AccountState.ACTIVE.value:
            return "portal_invite_skipped_active_account"
        if account_state == AccountState.SUSPENDED.value:
            return "portal_invite_skipped_suspended_account"
        if account_state == AccountState.DEACTIVATED.value:
            return "portal_invite_skipped_deactivated_account"
        return "portal_invite_skipped_existing_account"

    @staticmethod
    def normalize_approval_status(raw_status: str | None) -> str:
        return normalize_approval_status(
            raw_status,
            default=ApprovalStatus.PENDING.value,
        )

    async def _load_backend_v2_participant(self, external_student_id: str) -> dict | None:
        """Resolve cohort participant + course/registration from backend_v2 (source of truth)."""
        try:
            participant_pk = int(str(external_student_id).strip())
        except (TypeError, ValueError):
            return None

        statement = text(
            """
            SELECT
                p.id AS participant_id,
                LOWER(TRIM(p.email)) AS email,
                p.name AS full_name,
                p.cohort AS cohort,
                p.status AS source_status,
                p.payment_status AS payment_status,
                c.id AS course_id,
                c.name AS course_name,
                c.start_date AS course_start_date,
                r.id AS registration_id,
                r.name AS registration_name,
                r.cohort AS registration_cohort
            FROM cohort_participant AS p
            LEFT JOIN cohort_course AS c ON c.id = p.course_id
            LEFT JOIN cohort_registration AS r ON r.id = p.registration_id
            WHERE p.id = :participant_id
            LIMIT 1
            """
        )
        result = await self.session.execute(statement, {"participant_id": participant_pk})
        row = result.mappings().first()
        return dict(row) if row is not None else None

    @staticmethod
    def _apply_backend_participant_row(
        payload: OnboardingInviteRequest, row: dict
    ) -> OnboardingInviteRequest:
        """Overwrite invite payload fields from the participant's current registration."""
        email = (row.get("email") or payload.email or "").strip().lower()
        full_name = (row.get("full_name") or payload.full_name or "").strip()
        cohort = row.get("cohort") or row.get("registration_cohort") or payload.cohort
        course_name = (row.get("course_name") or payload.course_name or "").strip()
        source_status = row.get("source_status") or payload.approval_status
        course_start = row.get("course_start_date") or payload.class_start_date

        return payload.model_copy(
            update={
                "email": email,
                "full_name": full_name or payload.full_name,
                "cohort": cohort,
                "course_name": course_name or payload.course_name,
                "external_student_id": str(row.get("participant_id") or payload.external_student_id),
                "source_email": email,
                "approval_status": source_status or payload.approval_status,
                "class_start_date": course_start,
            }
        )

    async def invite_non_zk_student(
        self,
        *,
        payload: OnboardingInviteRequest,
    ) -> OnboardingInviteResponse:
        if payload.source_system == "backend_v2":
            participant_row = await self._load_backend_v2_participant(payload.external_student_id)
            if participant_row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Participant not found in admissions records",
                )
            if not participant_row.get("payment_status"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Participant has not completed payment",
                )
            if not (participant_row.get("course_name") or "").strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Participant has no course assigned",
                )
            payload = self._apply_backend_participant_row(payload, participant_row)

        if self.is_zk_course(payload.course_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ZK cohorts must not use the standard onboarding invite flow",
            )

        normalized_email = payload.email.lower().strip()
        normalized_approval_status = self.normalize_approval_status(payload.approval_status)
        user = await self._get_user_by_email(normalized_email)
        portal_invite_created = False

        if user is None:
            user = User(
                email=normalized_email,
                role=UserRole.STUDENT.value,
                account_state=AccountState.INVITED.value,
            )
            self.session.add(user)
            await self.session.flush()
            portal_invite_created = True

        current_account_state = user.account_state

        profile = await self._get_profile_by_user_id(user.id)
        if profile is None:
            profile = StudentProfile(
                user_id=user.id,
                full_name=payload.full_name,
                cohort=payload.cohort,
                onboarding_status=OnboardingStatus.INVITED.value,
            )
            self.session.add(profile)
        else:
            profile.full_name = payload.full_name
            profile.cohort = payload.cohort

        should_issue_activation_invite = self.should_issue_activation_invite(
            portal_invite_created=portal_invite_created,
            account_state=current_account_state,
            onboarding_status=profile.onboarding_status,
        )

        if (
            should_issue_activation_invite
            and profile.onboarding_status == OnboardingStatus.PENDING.value
        ):
            profile.onboarding_status = OnboardingStatus.INVITED.value

        external_map = await self._get_external_map(payload.external_student_id)
        if external_map is None:
            external_map = ExternalStudentMap(
                user_id=user.id,
                source_system=payload.source_system,
                external_student_id=payload.external_student_id,
                source_email=(payload.source_email or normalized_email).lower().strip(),
                approval_status=normalized_approval_status,
                approval_updated_at=datetime.now(UTC),
                last_synced_at=datetime.now(UTC),
            )
            self.session.add(external_map)
        else:
            external_map.user_id = user.id
            external_map.source_system = payload.source_system
            external_map.source_email = (payload.source_email or normalized_email).lower().strip()
            external_map.approval_status = normalized_approval_status
            external_map.approval_updated_at = datetime.now(UTC)
            external_map.last_synced_at = datetime.now(UTC)

        if portal_invite_created:
            self.session.add(
                StudentStatusHistory(
                    user_id=user.id,
                    from_state=current_account_state,
                    to_state=AccountState.INVITED.value,
                    reason="non_zk_payment_onboarding",
                    changed_at=datetime.now(UTC),
                )
            )
            user.account_state = AccountState.INVITED.value

        await self.session.commit()
        await self.session.refresh(user)
        await self.session.refresh(profile)

        activation_url: str | None = None
        if should_issue_activation_invite:
            activation_token = await self.auth_service.create_activation_token_for_user(user=user)
            activation_url = self.build_activation_url(activation_token)

            asyncio.create_task(
                self._send_onboarding_email_safe(
                    to_email=normalized_email,
                    student_name=payload.full_name,
                    activation_url=activation_url,
                    class_start_date=payload.class_start_date,
                )
            )

        reason = self.resolve_invite_reason(
            portal_invite_created=portal_invite_created,
            account_state=current_account_state,
            issued_invite=bool(activation_url),
        )

        self.session.add(
            AuditLog(
                actor_user_id=None,
                action=reason,
                resource_type="user",
                resource_id=str(user.id),
                after_json={
                    "email": user.email,
                    "cohort": payload.cohort,
                    "course_name": payload.course_name,
                    "external_student_id": payload.external_student_id,
                    "source_system": payload.source_system,
                },
                request_id=payload.external_student_id,
                created_at=datetime.now(UTC),
            )
        )
        await self.session.commit()

        return OnboardingInviteResponse(
            user_id=user.id,
            email=user.email,
            account_state=user.account_state,
            onboarding_status=profile.onboarding_status,
            activation_url=activation_url,
            portal_invite_created=portal_invite_created,
            reason=reason,
        )

    async def _get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def _get_profile_by_user_id(self, user_id: int) -> StudentProfile | None:
        statement = select(StudentProfile).where(StudentProfile.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def _get_external_map(self, external_student_id: str) -> ExternalStudentMap | None:
        statement = select(ExternalStudentMap).where(
            ExternalStudentMap.external_student_id == external_student_id
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def _send_onboarding_email_safe(
        self,
        *,
        to_email: str,
        student_name: str,
        activation_url: str,
        class_start_date: date | None = None,
    ) -> None:
        """Fire-and-forget wrapper — logs errors but never raises."""
        try:
            sent = await self.email_service.send_onboarding_email(
                to_email=to_email,
                student_name=student_name,
                activation_url=activation_url,
                class_start_date=class_start_date,
            )
            if not sent:
                logger.warning(
                    "Onboarding email was not sent to %s (service returned False)", to_email
                )
        except Exception:
            logger.exception("Failed to send onboarding email to %s", to_email)
