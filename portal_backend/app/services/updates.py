import asyncio
from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import (
    AuditLog,
    AccountState,
    StudentProfile,
    StudentUpdate,
    StudentUpdateRead,
    UpdateTargetType,
    User,
    UserRole,
)
from app.schemas.auth import MessageResponse
from app.schemas.updates import (
    CreateStudentUpdateRequest,
    MarkStudentUpdateReadResponse,
    StudentUpdateResponse,
    UpdateStudentUpdateRequest,
)


class UpdatesService:
    def __init__(self, session: AsyncSession, *, email_service: Any | None = None) -> None:
        self.session = session
        self.email_service = email_service
        if self.email_service is None:
            try:
                from app.services.email import EmailService

                self.email_service = EmailService()
            except ModuleNotFoundError:
                self.email_service = None

    async def create_update(
        self,
        *,
        actor: User,
        payload: CreateStudentUpdateRequest,
    ) -> StudentUpdateResponse:
        now = datetime.now(UTC)
        student_update = StudentUpdate(
            title=payload.title,
            body=payload.body,
            target_type=payload.target_type.value,
            target_ref=payload.target_ref,
            is_published=payload.is_published,
            send_in_app=payload.send_in_app,
            send_email=payload.send_email,
            published_at=now if payload.is_published else None,
            created_by=actor.id,
            created_at=now,
            updated_at=now,
        )
        self.session.add(student_update)
        await self.session.flush()

        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_update_created",
                resource_type="student_update",
                resource_id=str(student_update.id),
                after_json=self._update_audit_snapshot(student_update),
                created_at=now,
            )
        )

        await self.session.commit()
        await self.session.refresh(student_update)
        await self._dispatch_notification_emails_if_required(student_update=student_update)
        return self._build_update_response(student_update=student_update)

    async def list_updates(self) -> list[StudentUpdateResponse]:
        updates = await self._list_all_updates()
        return [self._build_update_response(student_update=item) for item in updates]

    async def get_update(self, *, update_id: int) -> StudentUpdateResponse:
        student_update = await self._get_update_by_id(update_id)
        return self._build_update_response(student_update=student_update)

    async def update_update(
        self,
        *,
        actor: User,
        update_id: int,
        payload: UpdateStudentUpdateRequest,
    ) -> StudentUpdateResponse:
        student_update = await self._get_update_by_id(update_id)
        before_json = self._update_audit_snapshot(student_update)
        updates = payload.model_dump(exclude_unset=True)

        for field_name, value in updates.items():
            if field_name == "target_type" and value is not None:
                setattr(student_update, field_name, value.value)
                continue
            setattr(student_update, field_name, value)

        send_in_app = (
            payload.send_in_app if payload.send_in_app is not None else student_update.send_in_app
        )
        send_email = (
            payload.send_email if payload.send_email is not None else student_update.send_email
        )
        if not send_in_app and not send_email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="At least one delivery channel must be enabled",
            )

        if payload.is_published is not None:
            student_update.published_at = datetime.now(UTC) if payload.is_published else None

        student_update.updated_at = datetime.now(UTC)

        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_update_updated",
                resource_type="student_update",
                resource_id=str(student_update.id),
                before_json=before_json,
                after_json=self._update_audit_snapshot(student_update),
                created_at=datetime.now(UTC),
            )
        )

        await self.session.commit()
        await self.session.refresh(student_update)
        await self._dispatch_notification_emails_if_required(student_update=student_update)
        return self._build_update_response(student_update=student_update)

    async def delete_update(self, *, actor: User, update_id: int) -> MessageResponse:
        student_update = await self._get_update_by_id(update_id)
        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_update_deleted",
                resource_type="student_update",
                resource_id=str(student_update.id),
                before_json=self._update_audit_snapshot(student_update),
                created_at=datetime.now(UTC),
            )
        )
        await self.session.delete(student_update)
        await self.session.commit()
        return MessageResponse(detail="Update deleted successfully")

    async def list_my_updates(self, *, user: User) -> list[StudentUpdateResponse]:
        if not hasattr(self.session, "execute"):
            profile = await self._get_profile_by_user_id(user.id)
            updates = await self._list_published_updates()
            visible_updates = [
                item
                for item in updates
                if self._update_applies_to_user(student_update=item, user=user, profile=profile)
            ]
            responses: list[StudentUpdateResponse] = []
            for item in visible_updates:
                read_record = await self._get_read_record(update_id=item.id, user_id=user.id)
                responses.append(
                    self._build_update_response(
                        student_update=item,
                        read_at=read_record.read_at if read_record is not None else None,
                    )
                )
            return responses

        profile = await self._get_profile_by_user_id(user.id)
        visibility_filters = [
            StudentUpdate.target_type == UpdateTargetType.ALL_ACTIVE.value,
            and_(
                StudentUpdate.target_type == UpdateTargetType.INDIVIDUAL.value,
                StudentUpdate.target_ref == str(user.id),
            ),
        ]
        if profile is not None and profile.cohort:
            visibility_filters.append(
                and_(
                    StudentUpdate.target_type == UpdateTargetType.COHORT.value,
                    StudentUpdate.target_ref == profile.cohort,
                )
            )

        result = await self.session.execute(
            select(StudentUpdate, StudentUpdateRead.read_at)
            .outerjoin(
                StudentUpdateRead,
                and_(
                    StudentUpdateRead.update_id == StudentUpdate.id,
                    StudentUpdateRead.user_id == user.id,
                ),
            )
            .where(
                StudentUpdate.is_published.is_(True),
                StudentUpdate.send_in_app.is_(True),
                or_(*visibility_filters),
            )
            .order_by(StudentUpdate.published_at.desc(), StudentUpdate.created_at.desc())
        )
        rows = result.all()
        return [
            self._build_update_response(student_update=student_update, read_at=read_at)
            for student_update, read_at in rows
        ]

    async def mark_update_as_read(
        self,
        *,
        user: User,
        update_id: int,
    ) -> MarkStudentUpdateReadResponse:
        profile = await self._get_profile_by_user_id(user.id)
        student_update = await self._get_update_by_id(update_id)
        if not student_update.is_published or not student_update.send_in_app or not self._update_applies_to_user(
            student_update=student_update,
            user=user,
            profile=profile,
        ):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update not found")

        read_record = await self._get_read_record(update_id=update_id, user_id=user.id)
        if read_record is None:
            read_record = StudentUpdateRead(
                update_id=update_id,
                user_id=user.id,
                read_at=datetime.now(UTC),
            )
            self.session.add(read_record)
            await self.session.commit()
            await self.session.refresh(read_record)

        return MarkStudentUpdateReadResponse(
            detail="Update marked as read",
            read_at=read_record.read_at,
        )

    async def _list_all_updates(self) -> list[StudentUpdate]:
        statement = select(StudentUpdate).order_by(StudentUpdate.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def _list_published_updates(self) -> list[StudentUpdate]:
        statement = select(StudentUpdate).where(
            StudentUpdate.is_published.is_(True),
            StudentUpdate.send_in_app.is_(True),
        )
        statement = statement.order_by(
            StudentUpdate.published_at.desc(),
            StudentUpdate.created_at.desc(),
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def _get_update_by_id(self, update_id: int) -> StudentUpdate:
        statement = select(StudentUpdate).where(StudentUpdate.id == update_id)
        result = await self.session.execute(statement)
        student_update = result.scalar_one_or_none()
        if student_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update not found")
        return student_update

    async def _get_profile_by_user_id(self, user_id: int) -> StudentProfile | None:
        statement = select(StudentProfile).where(StudentProfile.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def _get_read_record(self, *, update_id: int, user_id: int) -> StudentUpdateRead | None:
        statement = select(StudentUpdateRead).where(
            StudentUpdateRead.update_id == update_id,
            StudentUpdateRead.user_id == user_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def _update_applies_to_user(
        *,
        student_update: StudentUpdate,
        user: User,
        profile: StudentProfile | None,
    ) -> bool:
        if student_update.target_type == UpdateTargetType.ALL_ACTIVE.value:
            return True
        if student_update.target_type == UpdateTargetType.INDIVIDUAL.value:
            return student_update.target_ref == str(user.id)
        if student_update.target_type == UpdateTargetType.COHORT.value:
            return profile is not None and student_update.target_ref == profile.cohort
        return False

    @staticmethod
    def _build_update_response(
        *,
        student_update: StudentUpdate,
        read_at: datetime | None = None,
    ) -> StudentUpdateResponse:
        return StudentUpdateResponse(
            id=student_update.id,
            title=student_update.title,
            body=student_update.body,
            target_type=student_update.target_type,
            target_ref=student_update.target_ref,
            is_published=student_update.is_published,
            send_in_app=student_update.send_in_app,
            send_email=student_update.send_email,
            published_at=student_update.published_at,
            created_by=student_update.created_by,
            created_at=student_update.created_at,
            updated_at=student_update.updated_at,
            read_at=read_at,
        )

    @staticmethod
    def _update_audit_snapshot(student_update: StudentUpdate) -> dict[str, str | int | bool | None]:
        return {
            "title": student_update.title,
            "body": student_update.body,
            "target_type": student_update.target_type,
            "target_ref": student_update.target_ref,
            "is_published": student_update.is_published,
            "send_in_app": student_update.send_in_app,
            "send_email": student_update.send_email,
            "created_by": student_update.created_by,
        }

    async def _dispatch_notification_emails_if_required(self, *, student_update: StudentUpdate) -> None:
        if not student_update.is_published or not student_update.send_email:
            return

        recipients = await self._list_target_emails(student_update=student_update)
        if not recipients:
            return

        asyncio.create_task(
            self._send_update_email_batch(
                emails=recipients,
                title=student_update.title,
                body=student_update.body,
            )
        )

    async def _list_target_emails(self, *, student_update: StudentUpdate) -> list[str]:
        if student_update.target_type == UpdateTargetType.ALL_ACTIVE.value:
            result = await self.session.execute(
                select(User.email).where(
                    User.role == UserRole.STUDENT.value,
                    User.account_state == AccountState.ACTIVE.value,
                )
            )
            return [email for email in result.scalars().all() if email]

        if student_update.target_type == UpdateTargetType.INDIVIDUAL.value:
            if not student_update.target_ref:
                return []
            try:
                target_user_id = int(student_update.target_ref)
            except ValueError:
                return []
            result = await self.session.execute(
                select(User.email).where(
                    User.id == target_user_id,
                    User.role == UserRole.STUDENT.value,
                )
            )
            email = result.scalar_one_or_none()
            return [email] if email else []

        if student_update.target_type == UpdateTargetType.COHORT.value:
            if not student_update.target_ref:
                return []
            result = await self.session.execute(
                select(User.email)
                .join(StudentProfile, StudentProfile.user_id == User.id)
                .where(
                    User.role == UserRole.STUDENT.value,
                    StudentProfile.cohort == student_update.target_ref,
                )
            )
            return [email for email in result.scalars().all() if email]

        return []

    async def _send_update_email_batch(
        self,
        *,
        emails: list[str],
        title: str,
        body: str,
    ) -> None:
        unique_emails = list(dict.fromkeys(email.lower().strip() for email in emails if email))
        if self.email_service is None:
            return
        for to_email in unique_emails:
            try:
                await self.email_service.send_update_notification_email(
                    to_email=to_email,
                    title=title,
                    body=body,
                )
            except Exception:
                # Email service is already safe, but keep this guard for task-level robustness.
                pass
