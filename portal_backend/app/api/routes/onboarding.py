from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import verify_internal_api_key
from app.db.session import get_db_session
from app.schemas.onboarding import (
    OnboardingInviteRequest,
    OnboardingInviteResponse,
)
from app.services.onboarding import OnboardingService

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.post(
    "/invite",
    response_model=OnboardingInviteResponse,
    status_code=status.HTTP_200_OK,
    summary="Invite a paid student",
    description=(
        "Create a portal account for a paid student and "
        "send an activation email. Requires the internal API key "
        "via X-Internal-API-Key header. ZK students must be approved "
        "before an invite is sent."
    ),
)
async def invite_non_zk_student(
    payload: OnboardingInviteRequest,
    _: str = Depends(verify_internal_api_key),
    db: AsyncSession = Depends(get_db_session),
) -> OnboardingInviteResponse:
    service = OnboardingService(db)
    return await service.invite_non_zk_student(payload=payload)
