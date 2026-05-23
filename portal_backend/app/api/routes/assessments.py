from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    AutomationAuth,
    get_active_user_or_automation_api_key,
    get_current_active_user,
    get_current_verified_user,
)
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.assessments import (
    AssessmentResultDetailResponse,
    MentorGradeRequest,
    MentorGradeResponse,
    PublishedAssessmentResponse,
    SaveMentorAssessmentRequest,
    SaveMentorAssessmentResponse,
    StartAssessmentResponse,
    SubmitAssessmentRequest,
    SubmitAssessmentResponse,
)
from app.services.assessments import AssessmentService

router = APIRouter(tags=["Assessments"])


@router.put(
    "/admin/portal/mentor-assessments/{mentor_assessment_id}/save",
    response_model=SaveMentorAssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Save mentor assessment questions",
    description=(
        "Authenticate with a Bearer access token (mentor/staff/admin) or an "
        "automation API key via the API-Key header."
    ),
)
async def save_mentor_assessment(
    mentor_assessment_id: int,
    payload: SaveMentorAssessmentRequest,
    auth: AutomationAuth = Depends(get_active_user_or_automation_api_key),
    db: AsyncSession = Depends(get_db_session),
) -> SaveMentorAssessmentResponse:
    return await AssessmentService(db).save_mentor_assessment(
        actor=auth.user,
        mentor_assessment_id=mentor_assessment_id,
        payload=payload,
        bypass_mentor_access=auth.via_api_key,
    )


@router.post(
    "/admin/portal/mentor-assessments/{mentor_assessment_id}/publish",
    response_model=PublishedAssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Publish mentor assessment for students",
)
async def publish_mentor_assessment(
    mentor_assessment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session),
) -> PublishedAssessmentResponse:
    return await AssessmentService(db).publish_assessment(
        actor=current_user,
        mentor_assessment_id=mentor_assessment_id,
    )


@router.post(
    "/mentor-assessments/{mentor_assessment_id}/start",
    response_model=StartAssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Start a published mentor assessment",
)
async def start_assessment(
    mentor_assessment_id: int,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> StartAssessmentResponse:
    return await AssessmentService(db).start_assessment(
        student=current_user,
        mentor_assessment_id=mentor_assessment_id,
    )


@router.post(
    "/mentor-assessments/{mentor_assessment_id}/submit",
    response_model=SubmitAssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit assessment answers (auto-graded when Answer is set on questions)",
)
async def submit_assessment(
    mentor_assessment_id: int,
    payload: SubmitAssessmentRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> SubmitAssessmentResponse:
    return await AssessmentService(db).submit_assessment(
        student=current_user,
        mentor_assessment_id=mentor_assessment_id,
        payload=payload,
    )


@router.post(
    "/admin/portal/assessment-results/{result_id}/grade",
    response_model=MentorGradeResponse,
    status_code=status.HTTP_200_OK,
    summary="Mentor grade or re-grade a student assessment result",
)
async def mentor_grade_assessment_result(
    result_id: int,
    payload: MentorGradeRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session),
) -> MentorGradeResponse:
    return await AssessmentService(db).mentor_grade_result(
        actor=current_user,
        result_id=result_id,
        payload=payload,
    )


@router.get(
    "/assessment-results/{result_id}",
    response_model=AssessmentResultDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get assessment result details",
)
async def get_assessment_result(
    result_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session),
) -> AssessmentResultDetailResponse:
    return await AssessmentService(db).get_result_detail(actor=current_user, result_id=result_id)
