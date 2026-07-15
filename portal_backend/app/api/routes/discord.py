from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_system_admin_or_mentor_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.discord import (
    DiscordInviteGenerateRequest,
    DiscordInviteGenerateResponse,
    DiscordInviteRevokeResponse,
    PendingDiscordInviteStudentResponse,
)
from app.services.discord import DiscordService

router = APIRouter(prefix="/admin/discord", tags=["Discord Admin"])


@router.get(
    "/invites/pending",
    response_model=list[PendingDiscordInviteStudentResponse],
    status_code=status.HTTP_200_OK,
    summary="List students pending Discord invites",
    description=(
        "List students that still need a Discord invite link. "
        "Requires a system admin or active mentor Bearer token."
    ),
)
async def list_pending_discord_invites(
    limit: int = Query(default=100, ge=1, le=500),
    _: User = Depends(get_current_system_admin_or_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[PendingDiscordInviteStudentResponse]:
    service = DiscordService(db)
    return await service.list_pending_invites(limit=limit)


@router.post(
    "/invites/generate",
    response_model=DiscordInviteGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Store generated Discord invite",
    description=(
        "Persist a generated Discord invite link and optional Discord "
        "metadata for a student. Requires a system admin or active mentor "
        "Bearer token."
    ),
)
async def upsert_generated_discord_invite(
    payload: DiscordInviteGenerateRequest,
    _: User = Depends(get_current_system_admin_or_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> DiscordInviteGenerateResponse:
    service = DiscordService(db)
    return await service.upsert_generated_invite(payload=payload)


@router.post(
    "/invites/{user_id}/revoke",
    response_model=DiscordInviteRevokeResponse,
    status_code=status.HTTP_200_OK,
    summary="Revoke student Discord invite",
    description=(
        "Revoke a previously generated student Discord invite. "
        "Requires a system admin or active mentor Bearer token."
    ),
)
async def revoke_generated_discord_invite(
    user_id: int,
    _: User = Depends(get_current_system_admin_or_mentor_user),
    db: AsyncSession = Depends(get_db_session),
) -> DiscordInviteRevokeResponse:
    service = DiscordService(db)
    return await service.revoke_invite(user_id=user_id)
