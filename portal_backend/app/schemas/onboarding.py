from datetime import date

from pydantic import BaseModel, EmailStr, Field


class OnboardingInviteRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    cohort: str | None = Field(default=None, max_length=100)
    course_name: str = Field(min_length=1, max_length=255)
    external_student_id: str = Field(min_length=1, max_length=255)
    source_system: str = Field(default="backend_v2", min_length=1, max_length=100)
    source_email: EmailStr | None = None
    approval_status: str = Field(default="approved", min_length=1, max_length=20)
    class_start_date: date | None = Field(
        default=None,
        description="Course start date shown in the portal onboarding email",
    )


class OnboardingInviteResponse(BaseModel):
    user_id: int
    email: EmailStr
    account_state: str
    onboarding_status: str
    activation_url: str | None = None
    portal_invite_created: bool
    reason: str
