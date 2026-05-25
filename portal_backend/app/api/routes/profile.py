from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_verified_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.profile import (
    GenerateMyDiscordInviteRequest,
    GenerateMyDiscordInviteResponse,
    MyProfileResponse,
    UpdateMyProfileRequest,
)
from app.services.profile import ProfileService
from app.services.student_discord import StudentDiscordService

router = APIRouter(prefix="/me", tags=["Profile"])


@router.get(
    "/profile",
    response_model=MyProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get my profile",
    description=(
        "Return the authenticated student's full profile including "
        "name, phone, wallet address, cohort, and onboarding status."
    ),
)
async def get_my_profile(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> MyProfileResponse:
    service = ProfileService(db)
    return await service.get_my_profile(user=current_user)


@router.patch(
    "/profile",
    response_model=MyProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update my profile",
    description=(
        "Update the authenticated student's profile. Editable "
        "fields: phone, discord_id, wallet_address, bio. "
        "Use POST /me/discord-invite for Discord email and invite links."
    ),
)
async def update_my_profile(
    payload: UpdateMyProfileRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> MyProfileResponse:
    service = ProfileService(db)
    return await service.update_my_profile(user=current_user, payload=payload)


@router.post(
    "/discord-invite",
    response_model=GenerateMyDiscordInviteResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate my Discord invite",
    description=(
        "Creates a Discord invite for the authenticated student only. "
        "Requires discord_email (the email they will use on Discord). "
        "If they change discord_email, any previous invite is revoked first. "
        "Re-requesting with the same email returns the existing invite."
    ),
)
async def generate_my_discord_invite(
    payload: GenerateMyDiscordInviteRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db_session),
) -> GenerateMyDiscordInviteResponse:
    return await StudentDiscordService(db).generate_my_discord_invite(
        user=current_user,
        payload=payload,
    )
