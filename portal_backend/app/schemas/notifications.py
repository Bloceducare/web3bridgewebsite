from datetime import datetime

from pydantic import BaseModel


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
