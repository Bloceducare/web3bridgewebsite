from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.models.portal import UpdateTargetType


class StudentUpdateResponse(BaseModel):
    id: int
    title: str
    body: str
    target_type: str
    target_ref: str | None = None
    is_published: bool
    send_in_app: bool
    send_email: bool
    published_at: datetime | None = None
    created_by: int | None = None
    programme: str | None = None
    track: str | None = None
    target_role: str | None = None
    created_at: datetime
    updated_at: datetime
    read_at: datetime | None = None


class CreateStudentUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)
    target_type: UpdateTargetType
    target_ref: str | None = Field(default=None, max_length=255)
    is_published: bool = False
    send_in_app: bool = True
    send_email: bool = False
    programme: str = Field(min_length=1, max_length=255)
    track: str = Field(min_length=1, max_length=255)
    target_role: str | None = Field(default=None, max_length=50)

    @model_validator(mode="after")
    def validate_channels(self) -> "CreateStudentUpdateRequest":
        if not self.send_in_app and not self.send_email:
            raise ValueError("At least one delivery channel must be enabled")
        return self


class UpdateStudentUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    body: str | None = Field(default=None, min_length=1)
    target_type: UpdateTargetType | None = None
    target_ref: str | None = Field(default=None, max_length=255)
    is_published: bool | None = None
    send_in_app: bool | None = None
    send_email: bool | None = None
    programme: str | None = Field(default=None, min_length=1, max_length=255)
    track: str | None = Field(default=None, min_length=1, max_length=255)
    target_role: str | None = Field(default=None, max_length=50)


class MarkStudentUpdateReadResponse(BaseModel):
    detail: str
    read_at: datetime

