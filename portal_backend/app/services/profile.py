from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import AuditLog, StudentProfile, User
from app.schemas.profile import MyProfileResponse, UpdateMyProfileRequest


class ProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_my_profile(self, *, user: User) -> MyProfileResponse:
        profile = await self._get_profile_by_user_id(user.id)
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        return self._build_profile_response(user=user, profile=profile)

    async def update_my_profile(
        self,
        *,
        user: User,
        payload: UpdateMyProfileRequest,
    ) -> MyProfileResponse:
        profile = await self._get_profile_by_user_id(user.id)
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        before_json = self._profile_audit_snapshot(profile)

        updates = payload.model_dump(exclude_unset=True)
        for field_name, value in updates.items():
            setattr(profile, field_name, value)

        self.session.add(
            AuditLog(
                actor_user_id=user.id,
                action="profile_updated",
                resource_type="student_profile",
                resource_id=str(profile.id),
                before_json=before_json,
                after_json=self._profile_audit_snapshot(profile),
                created_at=datetime.now(UTC),
            )
        )

        await self.session.commit()
        await self.session.refresh(profile)

        return self._build_profile_response(user=user, profile=profile)

    async def _get_profile_by_user_id(self, user_id: int) -> StudentProfile | None:
        statement = select(StudentProfile).where(StudentProfile.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def _build_profile_response(*, user: User, profile: StudentProfile) -> MyProfileResponse:
        return MyProfileResponse(
            user_id=user.id,
            email=user.email,
            role=user.role,
            account_state=user.account_state,
            email_verified=user.email_verified,
            full_name=profile.full_name,
            phone=profile.phone,
            discord_id=profile.discord_id,
            discord_invite_link=profile.discord_invite_link,
            discord_email=profile.discord_email,
            discord_username=profile.discord_email,
            wallet_address=profile.wallet_address,
            cohort=profile.cohort,
            onboarding_status=profile.onboarding_status,
            participation=profile.participation,
            bio=profile.bio,
        )

    @staticmethod
    def _profile_audit_snapshot(profile: StudentProfile) -> dict[str, str | None]:
        return {
            "full_name": profile.full_name,
            "phone": profile.phone,
            "discord_id": profile.discord_id,
            "discord_invite_link": profile.discord_invite_link,
            "discord_email": profile.discord_email,
            "wallet_address": profile.wallet_address,
            "cohort": profile.cohort,
            "onboarding_status": profile.onboarding_status,
            "bio": profile.bio,
        }
