from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_staff_or_admin_user, get_current_verified_user
from app.db.session import get_db_session
from app.models.portal import NotificationScope, NotificationSenderType, UpdateTargetType
from app.models.portal import User
from app.schemas.notifications import (
    AdminAnnouncementCreateRequest,
    AdminAnnouncementResponse,
    MarkNotificationReadResponse,
    NotificationItemResponse,
    NotificationSummaryResponse,
)
from app.services.notifications import NotificationsService
from app.services.updates import UpdatesService
from app.schemas.updates import CreateStudentUpdateRequest

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get(
    "/my",
    response_model=list[NotificationItemResponse],
    status_code=status.HTTP_200_OK,
    summary="List my notifications",
    description="Return notification feed for the authenticated student.",
)
async def list_my_notifications(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[NotificationItemResponse]:
    service = NotificationsService(db)
    return await service.list_my_notifications(user=current_user)


@router.get(
    "/my/summary",
    response_model=NotificationSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get my notification summary",
    description="Return counts for total and unread notifications for the authenticated student.",
)
async def get_my_notification_summary(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> NotificationSummaryResponse:
    service = NotificationsService(db)
    return await service.get_my_summary(user=current_user)


@router.post(
    "/{notification_id}/read",
    response_model=MarkNotificationReadResponse,
    status_code=status.HTTP_200_OK,
    summary="Mark notification as read",
    description="Mark a notification as read for the authenticated student.",
)
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> MarkNotificationReadResponse:
    service = NotificationsService(db)
    return await service.mark_as_read(user=current_user, notification_id=notification_id)


@router.post(
    "/admin/announcements",
    response_model=AdminAnnouncementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create admin announcement",
    description=(
        "Create a platform-wide or course/cohort-scoped announcement. "
        "Mentor senders are restricted to course scope."
    ),
)
async def create_admin_announcement(
    payload: AdminAnnouncementCreateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> AdminAnnouncementResponse:
    if payload.sender_type == NotificationSenderType.MENTOR and payload.scope != NotificationScope.COURSE:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Mentor notifications must use course scope")

    if payload.scope == NotificationScope.PLATFORM:
        target_type = UpdateTargetType.ALL_ACTIVE
        target_ref = None
    else:
        target_type = UpdateTargetType.COHORT
        target_ref = payload.cohort or (f"course:{payload.course_id}" if payload.course_id else None)
        if target_ref is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="course_id or cohort is required for course scope announcements")

    update = await UpdatesService(db).create_update(
        actor=current_user,
        payload=CreateStudentUpdateRequest(
            title=payload.title,
            body=payload.body,
            target_type=target_type,
            target_ref=target_ref,
            is_published=payload.is_published,
            send_in_app=payload.send_in_app,
            send_email=payload.send_email,
        ),
    )
    return AdminAnnouncementResponse(detail="Announcement created", update_id=update.id)
