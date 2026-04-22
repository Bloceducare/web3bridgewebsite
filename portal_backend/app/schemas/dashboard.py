from datetime import datetime

from pydantic import BaseModel


class DashboardRecentStudentResponse(BaseModel):
    user_id: int
    full_name: str | None = None
    email: str
    cohort: str | None = None
    account_state: str
    created_at: datetime


class AdminDashboardOverviewResponse(BaseModel):
    total_students: int
    active_students: int
    suspended_students: int
    invited_students: int
    deactivated_students: int
    pending_discord_invites: int
    published_announcements: int
    recent_students: list[DashboardRecentStudentResponse]
