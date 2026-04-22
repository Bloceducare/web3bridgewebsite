from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import StudentProfile, StudentUpdate, StudentUpdateRead, UpdateTargetType, User
from app.schemas.notifications import (
    MarkNotificationReadResponse,
    NotificationItemResponse,
    NotificationSummaryResponse,
)


class NotificationsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_my_notifications(self, *, user: User) -> list[NotificationItemResponse]:
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

        statement = (
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
        result = await self.session.execute(statement)
        rows = result.all()

        return [
            NotificationItemResponse(
                id=student_update.id,
                title=student_update.title,
                body=student_update.body,
                is_read=read_at is not None,
                read_at=read_at,
                published_at=student_update.published_at,
                created_at=student_update.created_at,
            )
            for student_update, read_at in rows
        ]

    async def get_my_summary(self, *, user: User) -> NotificationSummaryResponse:
        notifications = await self.list_my_notifications(user=user)
        unread = sum(1 for item in notifications if not item.is_read)
        return NotificationSummaryResponse(total=len(notifications), unread=unread)

    async def mark_as_read(
        self,
        *,
        user: User,
        notification_id: int,
    ) -> MarkNotificationReadResponse:
        profile = await self._get_profile_by_user_id(user.id)
        update = await self._get_update(notification_id)
        if not update.is_published or not update.send_in_app or not self._update_applies_to_user(
            student_update=update,
            user=user,
            profile=profile,
        ):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

        read_record = await self._get_read_record(update_id=update.id, user_id=user.id)
        if read_record is None:
            read_record = StudentUpdateRead(
                update_id=update.id,
                user_id=user.id,
                read_at=datetime.now(UTC),
            )
            self.session.add(read_record)
            await self.session.commit()
            await self.session.refresh(read_record)

        return MarkNotificationReadResponse(detail="Notification marked as read", read_at=read_record.read_at)

    async def _get_profile_by_user_id(self, user_id: int) -> StudentProfile | None:
        result = await self.session.execute(select(StudentProfile).where(StudentProfile.user_id == user_id))
        return result.scalar_one_or_none()

    async def _get_read_record(self, *, update_id: int, user_id: int) -> StudentUpdateRead | None:
        result = await self.session.execute(
            select(StudentUpdateRead).where(
                StudentUpdateRead.update_id == update_id,
                StudentUpdateRead.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def _get_update(self, update_id: int) -> StudentUpdate:
        result = await self.session.execute(select(StudentUpdate).where(StudentUpdate.id == update_id))
        update = result.scalar_one_or_none()
        if update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return update

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
