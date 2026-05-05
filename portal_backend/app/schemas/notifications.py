from datetime import datetime

from pydantic import BaseModel, Field

from app.models.portal import NotificationScope, NotificationSenderType


class NotificationItemResponse(BaseModel):
    id: int
    title: str
    body: str
    is_read: bool
    read_at: datetime | None = None
    published_at: datetime | None = None
    created_at: datetime


class NotificationSummaryResponse(BaseModel):
    total: int
    unread: int


class MarkNotificationReadResponse(BaseModel):
    detail: str
    read_at: datetime


class AdminAnnouncementCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)
    scope: NotificationScope
    sender_type: NotificationSenderType
    course_id: int | None = None
    cohort: str | None = Field(default=None, max_length=100)
    is_published: bool = True
    send_in_app: bool = True
    send_email: bool = False


class AdminAnnouncementResponse(BaseModel):
    detail: str
    update_id: int
