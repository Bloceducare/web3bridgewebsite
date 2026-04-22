from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import verify_internal_api_key
from app.db.session import get_db_session
from app.schemas.discord import (
    DiscordInviteGenerateRequest,
    DiscordInviteGenerateResponse,
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
        "Internal endpoint for the Discord bot to fetch students "
        "that still need an invite link."
    ),
)
async def list_pending_discord_invites(
    limit: int = Query(default=100, ge=1, le=500),
    _: str = Depends(verify_internal_api_key),
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
        "Internal endpoint for the Discord bot to persist a generated "
        "invite link and optional Discord metadata for a student."
    ),
)
async def upsert_generated_discord_invite(
    payload: DiscordInviteGenerateRequest,
    _: str = Depends(verify_internal_api_key),
    db: AsyncSession = Depends(get_db_session),
) -> DiscordInviteGenerateResponse:
    service = DiscordService(db)
    return await service.upsert_generated_invite(payload=payload)
