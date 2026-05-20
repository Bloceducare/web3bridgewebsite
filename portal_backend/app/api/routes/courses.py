from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_staff_or_admin_user, get_current_verified_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.courses import (
    AdminCourseSummaryResponse,
    StudentCourseResponse,
    StudentGuarantorFormResponse,
)
from app.services.courses import CoursesService

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get(
    "/my",
    response_model=list[StudentCourseResponse],
    status_code=status.HTTP_200_OK,
    summary="List my courses",
    description=(
        "Return courses associated with the authenticated student "
        "using backend_v2 participant records."
    ),
)
async def list_my_courses(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[StudentCourseResponse]:
    service = CoursesService(db)
    return await service.list_my_courses(user=current_user)


@router.get(
    "/my/guarantor-form",
    response_model=StudentGuarantorFormResponse,
    status_code=status.HTTP_200_OK,
    summary="Get my published guarantor form",
    description=(
        "Return the latest active guarantor form for the authenticated student. "
        "Uses the student's latest participant cohort, then falls back to a generic form."
    ),
)
async def get_my_guarantor_form(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentGuarantorFormResponse:
    service = CoursesService(db)
    return await service.get_my_published_guarantor_form(user=current_user)


@router.get(
    "/admin/summary",
    response_model=list[AdminCourseSummaryResponse],
    status_code=status.HTTP_200_OK,
    summary="List admin course summaries",
    description="Return aggregate per-course enrollment metrics for staff/admin dashboards.",
)
async def list_admin_course_summaries(
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[AdminCourseSummaryResponse]:
    service = CoursesService(db)
    return await service.list_admin_course_summaries()
