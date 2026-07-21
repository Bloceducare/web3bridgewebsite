from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.discord_bot import DiscordBotClient, DiscordBotError, extract_discord_invite_code
from app.core.config import get_settings
from app.models.portal import AuditLog, StudentProfile, User, UserRole
from app.schemas.profile import GenerateMyDiscordInviteRequest, GenerateMyDiscordInviteResponse

settings = get_settings()


class StudentDiscordService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.discord_bot = DiscordBotClient()

    async def generate_my_discord_invite(
        self,
        *,
        user: User,
        payload: GenerateMyDiscordInviteRequest,
    ) -> GenerateMyDiscordInviteResponse:
        if user.role != UserRole.STUDENT.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student access required",
            )
        if not settings.DISCORD_BOT_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Discord invite service is not configured",
            )

        profile = await self._get_profile(user.id)
        discord_email = str(payload.discord_email).strip().lower()
        await self._ensure_discord_email_available(
            discord_email=discord_email,
            user_id=user.id,
        )

        previous_discord_email = (profile.discord_email or "").strip().lower()
        email_changed = previous_discord_email != discord_email
        replaced_previous_invite = False

        if email_changed and profile.discord_invite_link:
            await self._revoke_existing_invite(profile.discord_invite_link)
            replaced_previous_invite = True
            await self.session.refresh(profile)

        if not email_changed and profile.discord_invite_link:
            profile.discord_email = discord_email
            await self.session.commit()
            await self.session.refresh(profile)
            return GenerateMyDiscordInviteResponse(
                invite_url=profile.discord_invite_link,
                invite_code=extract_discord_invite_code(profile.discord_invite_link),
                discord_email=discord_email,
                replaced_previous_invite=False,
                message="Existing invite returned for your Discord email",
            )

        profile.discord_email = discord_email
        # Commit before calling discord-bot so we do not hold a row lock on
        # student_profiles while the bot updates discord_invite_link.
        await self.session.commit()
        await self.session.refresh(profile)

        try:
            invite_payload = await self.discord_bot.create_invite(
                email=user.email,
                user_id=user.id,
                role=settings.DISCORD_STUDENT_ROLE,
                category_id=settings.DISCORD_INVITE_CATEGORY_ID or None,
            )
        except DiscordBotError as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

        invite_url = str(
            invite_payload.get("invite_url")
            or invite_payload.get("invite_link")
            or ""
        )
        invite_code = invite_payload.get("invite_code") or extract_discord_invite_code(invite_url)

        # discord-bot owns discord_invite_link; refresh to read what it persisted.
        await self.session.refresh(profile)
        stored_invite_url = profile.discord_invite_link or invite_url

        self.session.add(
            AuditLog(
                actor_user_id=user.id,
                action="student_discord_invite_generated",
                resource_type="student_profile",
                resource_id=str(profile.id),
                after_json={
                    "discord_email": discord_email,
                    "discord_invite_link": stored_invite_url,
                    "role": settings.DISCORD_STUDENT_ROLE,
                    "replaced_previous_invite": replaced_previous_invite,
                    "profile_synced": invite_payload.get("profile_synced", True),
                },
                created_at=datetime.now(UTC),
            )
        )
        await self.session.commit()

        return GenerateMyDiscordInviteResponse(
            invite_url=stored_invite_url,
            invite_code=invite_code,
            discord_email=discord_email,
            replaced_previous_invite=replaced_previous_invite,
            message="Discord invite created",
        )

    async def _revoke_existing_invite(self, invite_link: str) -> None:
        invite_code = extract_discord_invite_code(invite_link)
        if not invite_code:
            return
        try:
            await self.discord_bot.revoke_invite(invite_code=invite_code)
        except DiscordBotError as exc:
            if exc.status_code != 404:
                raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    async def _ensure_discord_email_available(self, *, discord_email: str, user_id: int) -> None:
        statement = select(StudentProfile.id).where(
            func.lower(StudentProfile.discord_email) == discord_email,
            StudentProfile.user_id != user_id,
        )
        result = await self.session.execute(statement)
        if result.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This Discord email is already linked to another student account",
            )

    async def _get_profile(self, user_id: int) -> StudentProfile:
        statement = select(StudentProfile).where(StudentProfile.user_id == user_id)
        result = await self.session.execute(statement)
        profile = result.scalar_one_or_none()
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        return profile
