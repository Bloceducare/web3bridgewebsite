from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_verified_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.portal_management import CourseMaterialStructuredResponse
from app.schemas.student import StudentMentorResponse
from app.services.student import StudentPortalService

router = APIRouter(prefix="/student", tags=["Student"])


@router.get(
    "/materials",
    response_model=list[CourseMaterialStructuredResponse],
    status_code=status.HTTP_200_OK,
    summary="List my course materials",
    description=(
        "Return course materials for courses the authenticated student is enrolled in. "
        "Optionally filter by course_id; the student must be enrolled in that course."
    ),
)
async def list_student_materials(
    course_id: int | None = Query(default=None),
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[CourseMaterialStructuredResponse]:
    rows = await StudentPortalService(db).list_materials(
        user=current_user, course_id=course_id
    )
    return [
        CourseMaterialStructuredResponse(
            id=row.id,
            course_id=row.course_id,
            title=row.title,
            material={
                "type": row.material_type,
                "resource_url": row.resource_url,
                "content": row.content,
                "metadata": row.metadata_json,
            },
        )
        for row in rows
    ]


@router.get(
    "/mentors",
    response_model=list[StudentMentorResponse],
    status_code=status.HTTP_200_OK,
    summary="List my mentors",
    description=(
        "Return active mentors assigned to courses the authenticated student is "
        "enrolled in. Optionally filter by course_id."
    ),
)
async def list_student_mentors(
    course_id: int | None = Query(default=None),
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[StudentMentorResponse]:
    return await StudentPortalService(db).list_mentors(
        user=current_user, course_id=course_id
    )
