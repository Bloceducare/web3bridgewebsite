from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import AuditLog, StudentProfile, User, UserRole
from app.schemas.discord import (
    DiscordInviteGenerateRequest,
    DiscordInviteGenerateResponse,
    PendingDiscordInviteStudentResponse,
)


class DiscordService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_pending_invites(self, *, limit: int = 100) -> list[PendingDiscordInviteStudentResponse]:
        result = await self.session.execute(
            select(User, StudentProfile)
            .join(StudentProfile, StudentProfile.user_id == User.id)
            .where(
                User.role == UserRole.STUDENT.value,
                StudentProfile.discord_invite_link.is_(None),
            )
            .order_by(User.id.asc())
            .limit(limit)
        )
        rows = result.all()
        return [
            PendingDiscordInviteStudentResponse(
                user_id=user.id,
                full_name=profile.full_name,
                email=user.email,
                cohort=profile.cohort,
                discord_email=profile.discord_email,
                onboarding_status=profile.onboarding_status,
            )
            for user, profile in rows
        ]

    async def upsert_generated_invite(
        self,
        *,
        payload: DiscordInviteGenerateRequest,
    ) -> DiscordInviteGenerateResponse:
        result = await self.session.execute(
            select(User, StudentProfile)
            .join(StudentProfile, StudentProfile.user_id == User.id)
            .where(
                User.id == payload.user_id,
                User.role == UserRole.STUDENT.value,
            )
        )
        row = result.one_or_none()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        user, profile = row
        profile.discord_invite_link = str(payload.invite_link)
        if payload.discord_id is not None:
            profile.discord_id = payload.discord_id
        if payload.discord_email is not None:
            profile.discord_email = payload.discord_email

        now = datetime.now(UTC)
        self.session.add(
            AuditLog(
                actor_user_id=None,
                action="discord_invite_upserted_by_bot",
                resource_type="student_profile",
                resource_id=str(user.id),
                after_json={
                    "discord_invite_link": profile.discord_invite_link,
                    "discord_id": profile.discord_id,
                    "discord_email": profile.discord_email,
                },
                created_at=now,
            )
        )
        await self.session.commit()

        return DiscordInviteGenerateResponse(
            detail="Discord invite stored",
            user_id=user.id,
            invite_link=profile.discord_invite_link,
            updated_at=now,
        )
