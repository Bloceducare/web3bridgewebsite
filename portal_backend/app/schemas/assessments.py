from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.models.portal import AssessmentType, EvaluationMode, ResultReleaseMode


class AssessmentQuestionOptions(BaseModel):
    A: str = ""
    B: str = ""
    C: str = ""
    D: str = ""

    model_config = {"extra": "allow"}


class AssessmentQuestion(BaseModel):
    Assessment_ID: str | None = None
    Quiz_ID: str | None = None
    Question: str = Field(min_length=1)
    Options: AssessmentQuestionOptions | dict[str, str] = Field(default_factory=dict)
    Answer: str | None = None
    Type: str = ""
    Difficulty: str = ""
    Explanation: str = ""

    model_config = {"extra": "allow"}

    @field_validator("Options", mode="before")
    @classmethod
    def normalize_options(cls, value: Any) -> dict[str, str]:
        if value is None:
            return {}
        if isinstance(value, AssessmentQuestionOptions):
            return value.model_dump()
        if isinstance(value, dict):
            return {str(k): str(v) for k, v in value.items()}
        return {}


class SaveMentorAssessmentRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    duration_minutes: int = Field(default=60, ge=1, le=24 * 60)
    due_at: datetime | None = None
    questions: list[AssessmentQuestion] = Field(min_length=1)
    assessment_type: AssessmentType | None = None
    evaluation_mode: EvaluationMode | None = None
    result_release_mode: ResultReleaseMode | None = None
    accepted: bool | None = None


class SaveMentorAssessmentResponse(BaseModel):
    mentor_assessment_id: int
    title: str
    duration_minutes: int
    due_at: datetime | None
    total_questions: int
    questions: list[dict]


class PublishedAssessmentResponse(BaseModel):
    """``id`` is the mentor assessment row (the published assessment)."""

    id: int
    course_id: int
    title: str
    due_at: datetime
    duration_minutes: int
    total_questions: int
    released_at: datetime | None = None


class StudentAssessmentListItemResponse(BaseModel):
    """Published assessment summary for students — no question bodies or answer keys."""

    mentor_assessment_id: int
    course_id: int
    title: str
    assessment_type: str
    duration_minutes: int
    due_at: datetime | None
    total_questions: int
    released_at: datetime
    result_id: int | None = None
    status: str
    score: int | None = None
    max_score: int
    started_at: datetime | None = None
    expires_at: datetime | None = None
    submitted_at: datetime | None = None
    can_start: bool
    is_overdue: bool


class StartAssessmentResponse(BaseModel):
    result_id: int
    mentor_assessment_id: int
    started_at: datetime
    expires_at: datetime
    duration_minutes: int
    questions: list[dict]


class StudentAnswerItem(BaseModel):
    quiz_id: str | None = None
    assessment_id: str | None = None
    answer: str = Field(min_length=0)


class SubmitAssessmentRequest(BaseModel):
    answers: list[StudentAnswerItem] = Field(min_length=1)


class QuestionGradeBreakdown(BaseModel):
    quiz_id: str | None = None
    assessment_id: str | None = None
    correct: bool | None = None
    expected: str | None = None
    given: str | None = None
    auto_graded: bool = False
    mentor_override: bool = False


class SubmitAssessmentResponse(BaseModel):
    result_id: int
    mentor_assessment_id: int
    score: int
    max_score: int
    status: str
    submitted_at: datetime
    breakdown: list[QuestionGradeBreakdown]


class MentorGradeRequest(BaseModel):
    score: int | None = Field(default=None, ge=0)
    breakdown: list[QuestionGradeBreakdown] | None = None
    feedback: str | None = None


class MentorGradeResponse(BaseModel):
    result_id: int
    user_id: int
    mentor_assessment_id: int
    score: int
    max_score: int
    status: str
    breakdown: list[QuestionGradeBreakdown]
    graded_by_mentor: bool = True


class AssessmentResultDetailResponse(BaseModel):
    id: int
    mentor_assessment_id: int
    user_id: int
    score: int | None
    max_score: int
    status: str
    started_at: datetime | None
    expires_at: datetime | None
    submitted_at: datetime | None
    responses: dict
    breakdown: list[QuestionGradeBreakdown]
