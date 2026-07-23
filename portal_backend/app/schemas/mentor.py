from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.schemas.portal_management import CourseMaterialCreateRequest, CourseMaterialUpdateRequest


class CreateMentorUpdateRequest(BaseModel):
    course_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)
    is_published: bool = False
    send_in_app: bool = True
    send_email: bool = False
    programme: str = Field(min_length=1, max_length=255)
    track: str = Field(min_length=1, max_length=255)

    @model_validator(mode="after")
    def validate_channels(self) -> "CreateMentorUpdateRequest":
        if not self.send_in_app and not self.send_email:
            raise ValueError("At least one delivery channel must be enabled")
        return self



class MentorStudentResponse(BaseModel):
    participant_name: str
    email: str
    course_id: int
    course_name: str
    cohort: str | None = None
    approval_status: str | None = None
    payment_status: bool | None = None
    portal_user_id: int | None = None
    account_state: str | None = None
    source_updated_at: datetime | None = None
