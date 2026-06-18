from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_mentor_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.auth import MessageResponse
from app.schemas.courses import AdminCourseSummaryResponse
from app.schemas.mentor import CreateMentorUpdateRequest, MentorStudentResponse
from app.schemas.portal_management import (
    CourseMaterialCreateRequest,
    CourseMaterialResponse,
    CourseMaterialStructuredResponse,
    CourseMaterialUpdateRequest,
)
from app.schemas.students import StudentParticipationResponse, UpdateParticipationRequest
from app.schemas.updates import StudentUpdateResponse
from app.services.mentor import MentorPortalService

router = APIRouter(prefix="/mentor", tags=["Mentor"])


@router.post(
    "/updates",
    response_model=StudentUpdateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Broadcast update to course students",
    description=(
        "Create an announcement for students enrolled in an assigned course. "
        "Targets only participants on that course."
    ),
)
async def create_mentor_update(
    payload: CreateMentorUpdateRequest,
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentUpdateResponse:
    return await MentorPortalService(db).create_course_update(actor=current_user, payload=payload)


@router.get(
    "/updates",
    response_model=list[StudentUpdateResponse],
    status_code=status.HTTP_200_OK,
    summary="List course announcements",
    description=(
        "Return announcements the mentor created for assigned courses, "
        "including drafts. Optionally filter by course_id."
    ),
)
async def list_mentor_updates(
    course_id: int | None = Query(default=None),
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[StudentUpdateResponse]:
    return await MentorPortalService(db).list_course_updates(
        actor=current_user, course_id=course_id
    )


@router.get(
    "/courses/summary",
    response_model=list[AdminCourseSummaryResponse],
    status_code=status.HTTP_200_OK,
    summary="List assigned course summaries",
    description="Enrollment metrics for courses assigned to the authenticated mentor.",
)
async def list_mentor_course_summaries(
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[AdminCourseSummaryResponse]:
    return await MentorPortalService(db).list_course_summaries(actor=current_user)


@router.get(
    "/materials",
    response_model=list[CourseMaterialStructuredResponse],
    status_code=status.HTTP_200_OK,
    summary="List course materials for assigned courses",
)
async def list_mentor_materials(
    course_id: int | None = Query(default=None),
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[CourseMaterialStructuredResponse]:
    rows = await MentorPortalService(db).list_materials(actor=current_user, course_id=course_id)
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


@router.post(
    "/materials",
    response_model=CourseMaterialResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create course material for an assigned course",
)
async def create_mentor_material(
    payload: CourseMaterialCreateRequest,
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> CourseMaterialResponse:
    return await MentorPortalService(db).create_material(actor=current_user, payload=payload)


@router.patch(
    "/materials/{material_id}",
    response_model=CourseMaterialResponse,
    status_code=status.HTTP_200_OK,
    summary="Update course material for an assigned course",
)
async def update_mentor_material(
    material_id: int,
    payload: CourseMaterialUpdateRequest,
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> CourseMaterialResponse:
    return await MentorPortalService(db).update_material(
        actor=current_user, material_id=material_id, payload=payload
    )


@router.delete(
    "/materials/{material_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete course material for an assigned course",
)
async def delete_mentor_material(
    material_id: int,
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> MessageResponse:
    await MentorPortalService(db).delete_material(actor=current_user, material_id=material_id)
    return MessageResponse(detail="Course material deleted")


@router.get(
    "/students",
    response_model=list[MentorStudentResponse],
    status_code=status.HTTP_200_OK,
    summary="List students in assigned courses",
    description=(
        "Returns participants enrolled in courses assigned to the mentor, "
        "optionally filtered by course_id."
    ),
)
async def list_mentor_students(
    course_id: int | None = Query(default=None),
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[MentorStudentResponse]:
    return await MentorPortalService(db).list_students(actor=current_user, course_id=course_id)


@router.patch(
    "/students/{portal_user_id}/participation",
    response_model=StudentParticipationResponse,
    status_code=status.HTTP_200_OK,
    summary="Set participation mode for a student in an assigned course",
    description=(
        "Set a student's mode of participation to 'onsite', 'online', or null. "
        "The student must be enrolled in one of the mentor's assigned courses."
    ),
)
async def set_mentor_student_participation(
    portal_user_id: int,
    payload: UpdateParticipationRequest,
    current_user: User = Depends(get_current_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentParticipationResponse:
    return await MentorPortalService(db).set_student_participation(
        actor=current_user,
        portal_user_id=portal_user_id,
        participation=payload.participation,
    )
