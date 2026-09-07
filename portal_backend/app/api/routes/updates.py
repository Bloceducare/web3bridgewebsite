from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_active_user,
    get_current_staff_or_admin_user,
    get_current_verified_user,
    get_current_staff_admin_or_mentor_user,
)
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.auth import MessageResponse
from app.schemas.updates import (
    CreateStudentUpdateRequest,
    MarkStudentUpdateReadResponse,
    StudentUpdateResponse,
    UpdateStudentUpdateRequest,
)
from app.services.updates import UpdatesService

router = APIRouter(prefix="/updates", tags=["Updates"])


# ── Student endpoints ──────────────────────────────────────────────


@router.get(
    "/my",
    response_model=list[StudentUpdateResponse],
    status_code=status.HTTP_200_OK,
    summary="List my updates",
    description=(
        "Return published updates that target the authenticated "
        "student (by cohort, individually, or all_active). "
        "Includes read_at timestamp if already read."
    ),
)
async def list_my_updates(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[StudentUpdateResponse]:
    service = UpdatesService(db)
    return await service.list_my_updates(user=current_user)


@router.post(
    "/{update_id}/read",
    response_model=MarkStudentUpdateReadResponse,
    status_code=status.HTTP_200_OK,
    summary="Mark update as read",
    description="Mark a specific update as read for the authenticated student.",
)
async def mark_update_as_read(
    update_id: int,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> MarkStudentUpdateReadResponse:
    service = UpdatesService(db)
    return await service.mark_update_as_read(
        user=current_user, update_id=update_id
    )


# ── Staff / Admin endpoints ───────────────────────────────────────


@router.get(
    "",
    response_model=list[StudentUpdateResponse],
    status_code=status.HTTP_200_OK,
    summary="List all updates",
    description="Return all updates (published and drafts). Staff or admin only.",
)
async def list_updates(
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[StudentUpdateResponse]:
    service = UpdatesService(db)
    return await service.list_updates()


@router.post(
    "",
    response_model=StudentUpdateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create update",
    description=(
        "Create a new announcement or update. Set target_type to "
        "'all_active', 'cohort', or 'individual' and optionally "
        "provide target_ref. Staff or admin only."
    ),
)
async def create_update(
    payload: CreateStudentUpdateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentUpdateResponse:
    service = UpdatesService(db)
    return await service.create_update(actor=current_user, payload=payload)


@router.get(
    "/{update_id}",
    response_model=StudentUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get update",
    description="Return a single update by ID. Staff or admin only.",
)
async def get_update(
    update_id: int,
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentUpdateResponse:
    service = UpdatesService(db)
    return await service.get_update(update_id=update_id)


@router.patch(
    "/{update_id}",
    response_model=StudentUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Edit update",
    description=(
        "Update an existing announcement. Only provided fields "
        "are changed. Staff or admin only."
    ),
)
async def update_update(
    update_id: int,
    payload: UpdateStudentUpdateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> StudentUpdateResponse:
    service = UpdatesService(db)
    return await service.update_update(
        actor=current_user, update_id=update_id, payload=payload
    )


@router.delete(
    "/{update_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete update",
    description="Permanently delete an update. Staff or admin only.",
)
async def delete_update(
    update_id: int,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MessageResponse:
    service = UpdatesService(db)
    return await service.delete_update(
        actor=current_user, update_id=update_id
    )


@router.get(
    "/history/mentor",
    response_model=list[StudentUpdateResponse],
    status_code=status.HTTP_200_OK,
    summary="Get announcement history from mentors",
    description="Return all announcements created by mentors. Staff, admin, or mentor only.",
)
async def list_mentor_updates(
    _: User = Depends(get_current_staff_admin_or_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[StudentUpdateResponse]:
    service = UpdatesService(db)
    return await service.list_mentor_announcements()


@router.get(
    "/history/admin",
    response_model=list[StudentUpdateResponse],
    status_code=status.HTTP_200_OK,
    summary="Get announcement history from admins",
    description="Return all announcements created by admins or staff. Staff or admin only.",
)
async def list_admin_updates(
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[StudentUpdateResponse]:
    service = UpdatesService(db)
    return await service.list_admin_announcements()
