from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class PendingDiscordInviteStudentResponse(BaseModel):
    user_id: int
    full_name: str | None = None
    email: str
    cohort: str | None = None
    discord_email: str | None = None
    onboarding_status: str


class DiscordInviteGenerateRequest(BaseModel):
    user_id: int = Field(gt=0)
    invite_link: HttpUrl
    discord_id: str | None = Field(default=None, max_length=100)
    discord_email: str | None = Field(default=None, max_length=255)


class DiscordInviteGenerateResponse(BaseModel):
    detail: str
    user_id: int
    invite_link: str
    updated_at: datetime
