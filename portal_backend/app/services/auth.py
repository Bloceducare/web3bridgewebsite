import asyncio
import logging
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import (
    TokenType,
    create_access_token,
    create_activation_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.portal import (
    AccountState,
    AuditLog,
    OnboardingStatus,
    RefreshToken,
    StudentProfile,
    StudentStatusHistory,
    User,
)
from app.schemas.auth import (
    AuthResponse,
    AuthUserResponse,
    PasswordResetResponse,
    TokenResponse,
    VerifyEmailResponse,
)
from app.services.email import EmailService

settings = get_settings()
logger = logging.getLogger(__name__)

VERIFICATION_CODE_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        *,
        email_service: EmailService | None = None,
    ) -> None:
        self.session = session
        self.email_service = email_service or EmailService()

    async def login(self, *, email: str, password: str) -> AuthResponse:
        user = await self._get_user_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if user.account_state != AccountState.ACTIVE.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is not active",
            )

        return await self._issue_tokens_for_user(user)

    async def activate_account(self, *, token: str, password: str) -> AuthResponse:
        payload = decode_token(token, expected_type=TokenType.ACTIVATION)
        user = await self.get_user_by_id(int(payload["sub"]))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        token_jti = str(payload.get("jti", ""))
        if not user.activation_token_jti or user.activation_token_jti != token_jti:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Activation token is invalid or already used",
            )

        if (
            user.activation_token_expires_at is not None
            and user.activation_token_expires_at <= datetime.now(UTC)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Activation token has expired",
            )

        if user.account_state in {AccountState.SUSPENDED.value, AccountState.DEACTIVATED.value}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account cannot be activated in its current state",
            )

        previous_account_state = user.account_state
        profile = await self._get_profile_by_user_id(user.id)
        previous_onboarding_status = profile.onboarding_status if profile is not None else None

        user.password_hash = hash_password(password)
        user.account_state = AccountState.ACTIVE.value
        user.activation_token_jti = None
        user.activation_token_expires_at = None

        if profile is not None:
            profile.onboarding_status = OnboardingStatus.COMPLETED.value

        if previous_account_state != AccountState.ACTIVE.value:
            self.session.add(
                StudentStatusHistory(
                    user_id=user.id,
                    from_state=previous_account_state,
                    to_state=AccountState.ACTIVE.value,
                    reason="account_activated",
                    changed_at=datetime.now(UTC),
                )
            )

        self.session.add(
            AuditLog(
                actor_user_id=user.id,
                action="account_activated",
                resource_type="user",
                resource_id=str(user.id),
                before_json={
                    "account_state": previous_account_state,
                    "onboarding_status": previous_onboarding_status,
                    "activation_token_jti": token_jti,
                },
                after_json={
                    "account_state": user.account_state,
                    "onboarding_status": (
                        profile.onboarding_status
                        if profile is not None
                        else previous_onboarding_status
                    ),
                    "activation_token_jti": user.activation_token_jti,
                },
                created_at=datetime.now(UTC),
            )
        )

        await self._revoke_all_user_refresh_tokens(user.id)

        # Generate and store email verification code
        code = self._generate_verification_code()
        user.email_verification_code = code
        user.email_verification_expires_at = datetime.now(UTC) + timedelta(
            minutes=VERIFICATION_CODE_EXPIRE_MINUTES
        )

        await self.session.commit()
        await self.session.refresh(user)
        if profile is not None:
            await self.session.refresh(profile)

        # Fire-and-forget: send verification email
        student_name = profile.full_name if profile else user.email
        asyncio.create_task(
            self._send_verification_email_safe(
                to_email=user.email,
                student_name=student_name,
                code=code,
            )
        )

        return await self._issue_tokens_for_user(user)

    async def refresh(self, *, refresh_token: str) -> AuthResponse:
        payload = decode_token(refresh_token, expected_type=TokenType.REFRESH)
        user = await self.get_user_by_id(int(payload["sub"]))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        token_record = await self._get_refresh_token_record(payload["jti"])
        if token_record is None or token_record.revoked_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token revoked",
            )

        if token_record.expires_at <= datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
            )

        token_record.revoked_at = datetime.now(UTC)
        await self.session.commit()
        return await self._issue_tokens_for_user(user)

    async def logout(self, *, refresh_token: str) -> None:
        payload = decode_token(refresh_token, expected_type=TokenType.REFRESH)
        token_record = await self._get_refresh_token_record(payload["jti"])
        if token_record is None:
            return

        token_record.revoked_at = datetime.now(UTC)
        await self.session.commit()

    async def request_password_reset(self, *, email: str) -> PasswordResetResponse:
        generic_detail = (
            "If the account exists, a password reset email has been sent"
        )
        user = await self._get_user_by_email(email)
        if user is None:
            return PasswordResetResponse(detail=generic_detail)

        reset_token, _, _ = create_password_reset_token(user_id=user.id, email=user.email)
        profile = await self._get_profile_by_user_id(user.id)
        student_name = profile.full_name if profile else user.email
        reset_url = (
            f"{settings.PORTAL_FRONTEND_URL.rstrip('/')}"
            f"/reset-password?token={reset_token}"
        )

        asyncio.create_task(
            self._send_password_reset_email_safe(
                to_email=user.email,
                student_name=student_name,
                reset_url=reset_url,
            )
        )

        return PasswordResetResponse(detail=generic_detail)

    async def reset_password(self, *, token: str, new_password: str) -> None:
        payload = decode_token(token, expected_type=TokenType.PASSWORD_RESET)
        user = await self.get_user_by_id(int(payload["sub"]))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.password_hash = hash_password(new_password)
        await self._revoke_all_user_refresh_tokens(user.id)
        await self.session.commit()

    async def change_password(
        self,
        *,
        user: User,
        current_password: str,
        new_password: str,
    ) -> None:
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        user.password_hash = hash_password(new_password)
        await self._revoke_all_user_refresh_tokens(user.id)
        await self.session.commit()

    async def verify_email(self, *, user: User, code: str) -> VerifyEmailResponse:
        if user.email_verified:
            return VerifyEmailResponse(detail="Email already verified", email_verified=True)

        if not user.email_verification_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No verification code found. Please request a new one.",
            )

        if (
            user.email_verification_expires_at is not None
            and user.email_verification_expires_at <= datetime.now(UTC)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired. Please request a new one.",
            )

        if user.email_verification_code != code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code.",
            )

        user.email_verified = True
        user.email_verification_code = None
        user.email_verification_expires_at = None

        self.session.add(
            AuditLog(
                actor_user_id=user.id,
                action="email_verified",
                resource_type="user",
                resource_id=str(user.id),
                after_json={"email": user.email, "email_verified": True},
                created_at=datetime.now(UTC),
            )
        )

        await self.session.commit()
        await self.session.refresh(user)
        return VerifyEmailResponse(detail="Email verified successfully", email_verified=True)

    async def resend_verification_code(self, *, user: User) -> VerifyEmailResponse:
        if user.email_verified:
            return VerifyEmailResponse(detail="Email already verified", email_verified=True)

        code = self._generate_verification_code()
        user.email_verification_code = code
        user.email_verification_expires_at = datetime.now(UTC) + timedelta(
            minutes=VERIFICATION_CODE_EXPIRE_MINUTES
        )
        await self.session.commit()

        profile = await self._get_profile_by_user_id(user.id)
        student_name = profile.full_name if profile else user.email

        asyncio.create_task(
            self._send_verification_email_safe(
                to_email=user.email,
                student_name=student_name,
                code=code,
            )
        )

        return VerifyEmailResponse(
            detail="Verification code sent to your email",
            email_verified=False,
        )

    async def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_activation_token_for_user(self, *, user: User) -> str:
        token, token_jti, expires_at = create_activation_token(user_id=user.id, email=user.email)
        user.activation_token_jti = token_jti
        user.activation_token_expires_at = expires_at
        await self.session.flush()
        return token

    async def _issue_tokens_for_user(self, user: User) -> AuthResponse:
        access_token, _, _ = create_access_token(user_id=user.id, email=user.email, role=user.role)
        refresh_token, refresh_jti, refresh_expires_at = create_refresh_token(
            user_id=user.id,
            email=user.email,
            role=user.role,
        )
        self.session.add(
            RefreshToken(
                user_id=user.id,
                jti=refresh_jti,
                expires_at=refresh_expires_at,
                created_at=datetime.now(UTC),
            )
        )
        user.last_login_at = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(user)

        profile = await self._get_profile_by_user_id(user.id)

        return AuthResponse(
            user=AuthUserResponse(
                id=user.id,
                email=user.email,
                role=user.role,
                account_state=user.account_state,
                email_verified=user.email_verified,
                full_name=profile.full_name if profile else None,
                phone=profile.phone if profile else None,
                discord_id=profile.discord_id if profile else None,
                wallet_address=profile.wallet_address if profile else None,
                cohort=profile.cohort if profile else None,
                onboarding_status=profile.onboarding_status if profile else None,
                bio=profile.bio if profile else None,
            ),
            tokens=TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
        )

    async def _get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email.lower())
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def _get_profile_by_user_id(self, user_id: int) -> StudentProfile | None:
        statement = select(StudentProfile).where(StudentProfile.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def _get_refresh_token_record(self, jti: str) -> RefreshToken | None:
        statement = select(RefreshToken).where(RefreshToken.jti == jti)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def _generate_verification_code() -> str:
        return f"{secrets.randbelow(1000000):06d}"

    async def _send_password_reset_email_safe(
        self,
        *,
        to_email: str,
        student_name: str,
        reset_url: str,
    ) -> None:
        try:
            sent = await self.email_service.send_password_reset_email(
                to_email=to_email,
                student_name=student_name,
                reset_url=reset_url,
                expire_hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS,
            )
            if not sent:
                logger.warning("Password reset email was not sent to %s", to_email)
        except Exception:
            logger.exception("Failed to send password reset email to %s", to_email)

    async def _send_verification_email_safe(
        self,
        *,
        to_email: str,
        student_name: str,
        code: str,
    ) -> None:
        try:
            sent = await self.email_service.send_verification_email(
                to_email=to_email,
                student_name=student_name,
                code=code,
            )
            if not sent:
                logger.warning("Verification email not sent to %s", to_email)
        except Exception:
            logger.exception("Failed to send verification email to %s", to_email)

    async def _revoke_all_user_refresh_tokens(self, user_id: int) -> None:
        statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
        )
        result = await self.session.execute(statement)
        token_records = result.scalars().all()
        revoked_at = datetime.now(UTC)
        for token_record in token_records:
            token_record.revoked_at = revoked_at
