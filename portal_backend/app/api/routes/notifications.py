from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_verified_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.notifications import (
    MarkNotificationReadResponse,
    NotificationItemResponse,
    NotificationSummaryResponse,
)
from app.services.notifications import NotificationsService

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
