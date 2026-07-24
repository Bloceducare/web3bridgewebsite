import asyncio
from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select, text
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
            programme=payload.programme,
            track=payload.track,
            target_role=payload.target_role,
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
        student_update.is_deleted = True
        self.session.add(student_update)
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
        await self.session.commit()
        return MessageResponse(detail="Update deleted successfully")

    async def list_my_updates(self, *, user: User) -> list[StudentUpdateResponse]:
        profile = await self._get_profile_by_user_id(user.id)
        enrolled_course_ids = await self._list_enrolled_course_ids_for_email(user.email)

        course_names = set()
        if user.role == UserRole.STUDENT.value:
            stmt = text("""
                SELECT DISTINCT LOWER(TRIM(c.name))
                FROM cohort_participant AS p
                JOIN cohort_course AS c ON c.id = p.course_id
                WHERE LOWER(TRIM(p.email)) = :email
            """)
            res = await self.session.execute(stmt, {"email": user.email.lower().strip()})
            course_names = {row[0] for row in res.all() if row[0]}

        mentor_programme = None
        mentor_track = None
        if user.role == UserRole.MENTOR.value:
            from app.models.portal import Mentor
            res = await self.session.execute(select(Mentor).where(Mentor.user_id == user.id))
            mentor = res.scalar_one_or_none()
            if mentor:
                mentor_programme = mentor.programme
                mentor_track = mentor.track

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
                StudentUpdate.is_deleted.is_(False),
            )
            .order_by(StudentUpdate.published_at.desc(), StudentUpdate.created_at.desc())
        )
        rows = result.all()

        responses: list[StudentUpdateResponse] = []
        for student_update, read_at in rows:
            # 1. Target Role
            if student_update.target_role and student_update.target_role != user.role:
                continue

            # 2. Programme
            if student_update.programme:
                if user.role == UserRole.STUDENT.value:
                    if not profile or profile.cohort != student_update.programme:
                        continue
                elif user.role == UserRole.MENTOR.value:
                    if not mentor_programme or mentor_programme != student_update.programme:
                        continue

            # 3. Track
            if student_update.track:
                if user.role == UserRole.STUDENT.value:
                    if student_update.track.lower().strip() not in course_names:
                        continue
                elif user.role == UserRole.MENTOR.value:
                    if not mentor_track or mentor_track.lower().strip() != student_update.track.lower().strip():
                        continue

            # Check original target fallback
            if student_update.target_type == UpdateTargetType.INDIVIDUAL.value:
                if student_update.target_ref != str(user.id):
                    continue
            elif student_update.target_type == UpdateTargetType.COHORT.value:
                if not profile or profile.cohort != student_update.target_ref:
                    continue
            elif student_update.target_type == UpdateTargetType.COURSE.value:
                if not student_update.target_ref:
                    continue
                try:
                    course_id = int(student_update.target_ref)
                except ValueError:
                    continue
                if course_id not in enrolled_course_ids:
                    continue

            responses.append(
                self._build_update_response(student_update=student_update, read_at=read_at)
            )

        return responses


    async def mark_update_as_read(
        self,
        *,
        user: User,
        update_id: int,
    ) -> MarkStudentUpdateReadResponse:
        profile = await self._get_profile_by_user_id(user.id)
        enrolled_course_ids = await self._list_enrolled_course_ids_for_email(user.email)
        student_update = await self._get_update_by_id(update_id)
        if not student_update.is_published or not student_update.send_in_app or not self._update_applies_to_user(
            student_update=student_update,
            user=user,
            profile=profile,
            enrolled_course_ids=enrolled_course_ids,
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
        statement = (
            select(StudentUpdate)
            .where(StudentUpdate.is_deleted.is_(False))
            .order_by(StudentUpdate.created_at.desc())
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def _list_published_updates(self) -> list[StudentUpdate]:
        statement = select(StudentUpdate).where(
            StudentUpdate.is_published.is_(True),
            StudentUpdate.send_in_app.is_(True),
            StudentUpdate.is_deleted.is_(False),
        )
        statement = statement.order_by(
            StudentUpdate.published_at.desc(),
            StudentUpdate.created_at.desc(),
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def _get_update_by_id(self, update_id: int) -> StudentUpdate:
        statement = select(StudentUpdate).where(
            StudentUpdate.id == update_id,
            StudentUpdate.is_deleted.is_(False),
        )
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
        enrolled_course_ids: set[int] | None = None,
    ) -> bool:
        if student_update.target_type == UpdateTargetType.ALL_ACTIVE.value:
            return True
        if student_update.target_type == UpdateTargetType.INDIVIDUAL.value:
            return student_update.target_ref == str(user.id)
        if student_update.target_type == UpdateTargetType.COHORT.value:
            return profile is not None and student_update.target_ref == profile.cohort
        if student_update.target_type == UpdateTargetType.COURSE.value:
            if not student_update.target_ref:
                return False
            try:
                course_id = int(student_update.target_ref)
            except ValueError:
                return False
            return course_id in (enrolled_course_ids or set())
        return False

    async def _list_enrolled_course_ids_for_email(self, email: str) -> set[int]:
        if not hasattr(self.session, "execute"):
            return set()
        statement = text(
            """
            SELECT DISTINCT p.course_id
            FROM cohort_participant AS p
            WHERE LOWER(TRIM(p.email)) = :email
              AND p.course_id IS NOT NULL
            """
        )
        result = await self.session.execute(
            statement, {"email": email.lower().strip()}
        )
        return {int(course_id) for course_id in result.scalars().all() if course_id is not None}

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
            programme=student_update.programme,
            track=student_update.track,
            target_role=student_update.target_role,
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
            "programme": student_update.programme,
            "track": student_update.track,
            "target_role": student_update.target_role,
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

        if student_update.target_type == UpdateTargetType.COURSE.value:
            if not student_update.target_ref:
                return []
            try:
                course_id = int(student_update.target_ref)
            except ValueError:
                return []
            result = await self.session.execute(
                text(
                    """
                    SELECT DISTINCT LOWER(TRIM(p.email)) AS email
                    FROM cohort_participant AS p
                    WHERE p.course_id = :course_id
                    """
                ),
                {"course_id": course_id},
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
