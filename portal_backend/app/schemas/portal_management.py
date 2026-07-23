from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, HttpUrl, model_validator

from app.models.portal import (
    AssessmentType,
    CourseMaterialType,
    EvaluationMode,
    ResultReleaseMode,
    UserRole,
)


class MentorCreateRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=3, max_length=255)
    bio: str | None = None
    is_active: bool = True
    programme: str | None = Field(default=None, max_length=255)
    track: str | None = Field(default=None, max_length=255)


class MentorUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    bio: str | None = None
    is_active: bool | None = None
    programme: str | None = Field(default=None, max_length=255)
    track: str | None = Field(default=None, max_length=255)


class MentorResponse(BaseModel):
    id: int
    full_name: str
    email: str
    bio: str | None = None
    is_active: bool
    programme: str | None = None
    track: str | None = None
    created_at: datetime
    updated_at: datetime
    course_ids: list[int] = []



class MentorCourseAssignRequest(BaseModel):
    course_id: int = Field(gt=0)


class CourseMaterialCreateRequest(BaseModel):
    course_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    material_type: CourseMaterialType
    resource_url: HttpUrl | None = None
    content: str | None = None
    metadata: dict = {}


class CourseMaterialUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    material_type: CourseMaterialType | None = None
    resource_url: HttpUrl | None = None
    content: str | None = None
    metadata: dict | None = None


class CourseMaterialResponse(BaseModel):
    id: int
    course_id: int
    title: str
    material_type: str
    resource_url: str | None = None
    content: str | None = None
    metadata: dict
    created_at: datetime
    updated_at: datetime


class CourseMaterialStructuredResponse(BaseModel):
    id: int
    course_id: int
    title: str
    material: dict


class MentorAssessmentCreateRequest(BaseModel):
    mentor_id: int = Field(gt=0)
    course_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    special_prompt: str | None = None
    assessment_type: AssessmentType = AssessmentType.MULTIPLE_CHOICE
    evaluation_mode: EvaluationMode = EvaluationMode.AI
    result_release_mode: ResultReleaseMode = ResultReleaseMode.MENTOR_CONTROLLED
    accepted: bool = False


class MentorAssessmentUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    special_prompt: str | None = None
    assessment_type: AssessmentType | None = None
    evaluation_mode: EvaluationMode | None = None
    result_release_mode: ResultReleaseMode | None = None
    accepted: bool | None = None


class MentorAssessmentResponse(BaseModel):
    id: int
    mentor_id: int
    course_id: int
    title: str
    special_prompt: str | None = None
    assessment_type: str
    evaluation_mode: str
    result_release_mode: str
    accepted: bool
    released_at: datetime | None = None
    duration_minutes: int
    due_at: datetime | None = None
    total_questions: int
    created_at: datetime
    updated_at: datetime


class GuarantorFormCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    form_url: HttpUrl
    cohort: str | None = Field(default=None, max_length=100)
    is_active: bool = True


class GuarantorFormUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    form_url: HttpUrl | None = None
    cohort: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class GuarantorFormResponse(BaseModel):
    id: int
    title: str
    form_url: str
    cohort: str | None = None
    is_active: bool
    uploaded_by: int | None = None
    created_at: datetime
    updated_at: datetime


class InvitePortalUserRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    full_name: str = Field(min_length=1, max_length=255)
    role: UserRole
    bio: str | None = None
    course_id: int | None = Field(
        default=None,
        gt=0,
        description="When inviting a mentor, assign this course on activation",
    )
    programme: str | None = Field(default=None, max_length=255)
    track: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def validate_mentor_course(self) -> "InvitePortalUserRequest":
        if self.course_id is not None and self.role != UserRole.MENTOR:
            raise ValueError("course_id is only supported when inviting a mentor")
        if (self.programme is not None or self.track is not None) and self.role != UserRole.MENTOR:
            raise ValueError("programme and track are only supported when inviting a mentor")
        return self



class InviteStudentByEmailRequest(BaseModel):
    """Admin-only invite: same backend path as paid non-ZK onboarding, email only."""

    email: EmailStr


class InvitePortalUserResponse(BaseModel):
    user_id: int
    email: str
    role: str
    account_state: str
    activation_url: str
