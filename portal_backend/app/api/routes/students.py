from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_staff_or_admin_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.students import (
    ArchiveStudentRequest,
    CreateStudentRequest,
    DeleteStudentResponse,
    EvictStudentRequest,
    StudentResponse,
    UpdateParticipationRequest,
    UpdateStudentRequest,
)
from app.services.students import StudentsService

router = APIRouter(prefix="/students", tags=["Students"])


@router.get(
    "",
    response_model=list[StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="List all students",
    description="Return all student accounts. Staff or admin only.",
)
async def list_students(
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[StudentResponse]:
    service = StudentsService(db)
    return await service.list_students()


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create student",
    description="Create a new student account/profile. Staff or admin only.",
)
async def create_student(
    payload: CreateStudentRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentResponse:
    service = StudentsService(db)
    return await service.create_student(actor=current_user, payload=payload)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get student details",
    description="Return a single student's profile. Staff or admin only.",
)
async def get_student(
    student_id: int,
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentResponse:
    service = StudentsService(db)
    return await service.get_student(student_id=student_id)


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update student",
    description=(
        "Update a student's profile or account state. Staff or "
        "admin only. Only provided fields are updated."
    ),
)
async def update_student(
    student_id: int,
    payload: UpdateStudentRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentResponse:
    service = StudentsService(db)
    return await service.update_student(
        actor=current_user, student_id=student_id, payload=payload
    )


@router.patch(
    "/{student_id}/participation",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Set student participation mode",
    description=(
        "Set a student's mode of participation to 'onsite', 'online', or null. "
        "Staff or admin only."
    ),
)
async def set_student_participation(
    student_id: int,
    payload: UpdateParticipationRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentResponse:
    service = StudentsService(db)
    return await service.set_participation(
        actor=current_user, student_id=student_id, participation=payload.participation
    )


@router.post(
    "/{student_id}/archive",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Archive student",
    description=(
        "Deactivate a student account. Sets account_state to "
        "DEACTIVATED. Staff or admin only."
    ),
)
async def archive_student(
    student_id: int,
    payload: ArchiveStudentRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentResponse:
    service = StudentsService(db)
    return await service.archive_student(
        actor=current_user, student_id=student_id, payload=payload
    )


@router.post(
    "/{student_id}/evict",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Evict student",
    description="Suspend a student account immediately. Staff or admin only.",
)
async def evict_student(
    student_id: int,
    payload: EvictStudentRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentResponse:
    return await StudentsService(db).evict_student(
        actor=current_user, student_id=student_id, reason=payload.reason
    )


@router.post(
    "/{student_id}/reinstate",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Reinstate student",
    description="Move a suspended/deactivated student back to active. Staff or admin only.",
)
async def reinstate_student(
    student_id: int,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentResponse:
    return await StudentsService(db).reinstate_student(
        actor=current_user, student_id=student_id
    )


@router.delete(
    "/{student_id}",
    response_model=DeleteStudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete student",
    description="Permanently delete student account and profile. Staff or admin only.",
)
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> DeleteStudentResponse:
    await StudentsService(db).delete_student(actor=current_user, student_id=student_id)
    return DeleteStudentResponse(detail="Student deleted")
