from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import (
    AccountState,
    AuditLog,
    StudentProfile,
    StudentStatusHistory,
    User,
    UserRole,
)
from app.schemas.students import (
    ArchiveStudentRequest,
    CreateStudentRequest,
    StudentResponse,
    UpdateStudentRequest,
)


class StudentsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_students(self) -> list[StudentResponse]:
        users = await self._list_student_users()
        students: list[StudentResponse] = []
        for user in users:
            profile = await self._get_profile_by_user_id(user.id)
            students.append(self._build_student_response(user=user, profile=profile))
        return students

    async def create_student(self, *, actor: User, payload: CreateStudentRequest) -> StudentResponse:
        normalized_email = payload.email.strip().lower()
        existing = await self.session.execute(select(User).where(User.email == normalized_email))
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student already exists")

        user = User(
            email=normalized_email,
            role=UserRole.STUDENT.value,
            account_state=payload.account_state.value,
            email_verified=payload.email_verified,
        )
        self.session.add(user)
        await self.session.flush()

        profile = StudentProfile(
            user_id=user.id,
            full_name=payload.full_name,
            phone=payload.phone,
            discord_email=str(payload.discord_email) if payload.discord_email else None,
            wallet_address=payload.wallet_address,
            cohort=payload.cohort,
            onboarding_status=payload.onboarding_status.value,
        )
        self.session.add(profile)
        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_created",
                resource_type="student",
                resource_id=str(user.id),
                after_json=self._student_audit_snapshot(user=user, profile=profile),
                created_at=datetime.now(UTC),
            )
        )
        await self.session.commit()
        await self.session.refresh(user)
        await self.session.refresh(profile)
        return self._build_student_response(user=user, profile=profile)

    async def get_student(self, *, student_id: int) -> StudentResponse:
        user = await self._get_student_by_id(student_id)
        profile = await self._get_profile_by_user_id(user.id)
        return self._build_student_response(user=user, profile=profile)

    async def update_student(
        self,
        *,
        actor: User,
        student_id: int,
        payload: UpdateStudentRequest,
    ) -> StudentResponse:
        user = await self._get_student_by_id(student_id)
        profile = await self._get_profile_by_user_id(user.id)
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        before_json = self._student_audit_snapshot(user=user, profile=profile)
        updates = payload.model_dump(exclude_unset=True)

        account_state = updates.pop("account_state", None)
        if account_state is not None and account_state != user.account_state:
            previous_state = user.account_state
            user.account_state = account_state
            self.session.add(
                StudentStatusHistory(
                    user_id=user.id,
                    from_state=previous_state,
                    to_state=account_state,
                    reason="student_updated_by_staff",
                    changed_by=actor.id,
                    changed_at=datetime.now(UTC),
                )
            )

        for field_name, value in updates.items():
            setattr(profile, field_name, value)

        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_updated",
                resource_type="student",
                resource_id=str(user.id),
                before_json=before_json,
                after_json=self._student_audit_snapshot(user=user, profile=profile),
                created_at=datetime.now(UTC),
            )
        )

        await self.session.commit()
        await self.session.refresh(user)
        await self.session.refresh(profile)
        return self._build_student_response(user=user, profile=profile)

    async def archive_student(
        self,
        *,
        actor: User,
        student_id: int,
        payload: ArchiveStudentRequest,
    ) -> StudentResponse:
        user = await self._get_student_by_id(student_id)
        profile = await self._get_profile_by_user_id(user.id)
        previous_state = user.account_state

        user.account_state = AccountState.DEACTIVATED.value

        if previous_state != AccountState.DEACTIVATED.value:
            self.session.add(
                StudentStatusHistory(
                    user_id=user.id,
                    from_state=previous_state,
                    to_state=AccountState.DEACTIVATED.value,
                    reason=payload.reason,
                    changed_by=actor.id,
                    changed_at=datetime.now(UTC),
                )
            )

        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_archived",
                resource_type="student",
                resource_id=str(user.id),
                before_json={"account_state": previous_state},
                after_json={"account_state": user.account_state, "reason": payload.reason},
                created_at=datetime.now(UTC),
            )
        )

        await self.session.commit()
        await self.session.refresh(user)
        if profile is not None:
            await self.session.refresh(profile)

        return self._build_student_response(user=user, profile=profile)

    async def evict_student(
        self,
        *,
        actor: User,
        student_id: int,
        reason: str | None = None,
    ) -> StudentResponse:
        user = await self._get_student_by_id(student_id)
        profile = await self._get_profile_by_user_id(user.id)
        previous_state = user.account_state
        user.account_state = AccountState.SUSPENDED.value
        self.session.add(
            StudentStatusHistory(
                user_id=user.id,
                from_state=previous_state,
                to_state=AccountState.SUSPENDED.value,
                reason=reason or "evicted_by_system_admin",
                changed_by=actor.id,
                changed_at=datetime.now(UTC),
            )
        )
        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_evicted",
                resource_type="student",
                resource_id=str(user.id),
                before_json={"account_state": previous_state},
                after_json={"account_state": user.account_state, "reason": reason},
                created_at=datetime.now(UTC),
            )
        )
        await self.session.commit()
        await self.session.refresh(user)
        if profile is not None:
            await self.session.refresh(profile)
        return self._build_student_response(user=user, profile=profile)

    async def reinstate_student(self, *, actor: User, student_id: int) -> StudentResponse:
        user = await self._get_student_by_id(student_id)
        profile = await self._get_profile_by_user_id(user.id)
        previous_state = user.account_state
        user.account_state = AccountState.ACTIVE.value
        self.session.add(
            StudentStatusHistory(
                user_id=user.id,
                from_state=previous_state,
                to_state=AccountState.ACTIVE.value,
                reason="reinstated_by_system_admin",
                changed_by=actor.id,
                changed_at=datetime.now(UTC),
            )
        )
        await self.session.commit()
        await self.session.refresh(user)
        if profile is not None:
            await self.session.refresh(profile)
        return self._build_student_response(user=user, profile=profile)

    async def delete_student(self, *, actor: User, student_id: int) -> None:
        user = await self._get_student_by_id(student_id)
        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_deleted",
                resource_type="student",
                resource_id=str(user.id),
                before_json={"email": user.email, "account_state": user.account_state},
                created_at=datetime.now(UTC),
            )
        )
        await self.session.delete(user)
        await self.session.commit()

    async def _list_student_users(self) -> list[User]:
        statement = select(User).where(User.role == UserRole.STUDENT.value).order_by(User.id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def _get_student_by_id(self, student_id: int) -> User:
        statement = select(User).where(User.id == student_id, User.role == UserRole.STUDENT.value)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return user

    async def _get_profile_by_user_id(self, user_id: int) -> StudentProfile | None:
        statement = select(StudentProfile).where(StudentProfile.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def _build_student_response(*, user: User, profile: StudentProfile | None) -> StudentResponse:
        return StudentResponse(
            user_id=user.id,
            email=user.email,
            role=user.role,
            account_state=user.account_state,
            full_name=profile.full_name if profile is not None else None,
            phone=profile.phone if profile is not None else None,
            discord_id=profile.discord_id if profile is not None else None,
            discord_invite_link=profile.discord_invite_link if profile is not None else None,
            discord_email=profile.discord_email if profile is not None else None,
            wallet_address=profile.wallet_address if profile is not None else None,
            cohort=profile.cohort if profile is not None else None,
            onboarding_status=profile.onboarding_status if profile is not None else None,
            bio=profile.bio if profile is not None else None,
        )

    @staticmethod
    def _student_audit_snapshot(
        *,
        user: User,
        profile: StudentProfile | None,
    ) -> dict[str, str | None]:
        return {
            "email": user.email,
            "account_state": user.account_state,
            "full_name": profile.full_name if profile is not None else None,
            "phone": profile.phone if profile is not None else None,
            "discord_id": profile.discord_id if profile is not None else None,
            "discord_invite_link": profile.discord_invite_link if profile is not None else None,
            "discord_email": profile.discord_email if profile is not None else None,
            "wallet_address": profile.wallet_address if profile is not None else None,
            "cohort": profile.cohort if profile is not None else None,
            "onboarding_status": profile.onboarding_status if profile is not None else None,
            "bio": profile.bio if profile is not None else None,
        }
