from pydantic import BaseModel, EmailStr, Field


class MyProfileResponse(BaseModel):
    user_id: int
    email: str
    role: str
    account_state: str
    email_verified: bool = False
    full_name: str
    phone: str | None = None
    discord_id: str | None = None
    discord_invite_link: str | None = None
    discord_email: str | None = None  # legacy column name; stores Discord username
    discord_username: str | None = None
    wallet_address: str | None = None
    cohort: str | None = None
    onboarding_status: str
    participation: str | None = None
    bio: str | None = None


class UpdateMyProfileRequest(BaseModel):
    phone: str | None = Field(default=None, max_length=20)
    discord_id: str | None = Field(default=None, max_length=100)
    wallet_address: str | None = Field(default=None, max_length=255)
    bio: str | None = None


class GenerateMyDiscordInviteRequest(BaseModel):
    discord_username: str = Field(..., min_length=1, max_length=100)


class GenerateMyDiscordInviteResponse(BaseModel):
    invite_url: str
    invite_code: str | None = None
    discord_username: str
    replaced_previous_invite: bool = False
    message: str
    role_assigned: bool = False
