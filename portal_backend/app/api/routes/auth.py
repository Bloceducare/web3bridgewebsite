from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.session import get_db_session
from app.models.portal import StudentProfile, User
from app.schemas.auth import (
    ActivationRequest,
    AuthResponse,
    AuthUserResponse,
    ChangePasswordRequest,
    LoginRequest,
    LogoutRequest,
    LogoutResponse,
    MessageResponse,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    PasswordResetResponse,
    RefreshRequest,
    ResendVerificationRequest,
    VerifyEmailRequest,
    VerifyEmailResponse,
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/activate",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Activate account",
    description=(
        "Activate a student portal account using the activation token "
        "from the onboarding email. Sets the account password and "
        "transitions the account state from INVITED to ACTIVE. "
        "Returns access and refresh tokens on success."
    ),
)
async def activate_account(
    payload: ActivationRequest,
    db: AsyncSession = Depends(get_db_session),
) -> AuthResponse:
    service = AuthService(db)
    return await service.activate_account(token=payload.token, password=payload.password)


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login",
    description="Authenticate with email and password. Only ACTIVE accounts can log in. "
    "Returns access and refresh JWT tokens.",
)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
) -> AuthResponse:
    service = AuthService(db)
    return await service.login(email=payload.email, password=payload.password)


@router.post(
    "/refresh",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh tokens",
    description=(
        "Exchange a valid refresh token for a new access/refresh "
        "token pair. The old refresh token is revoked after use."
    ),
)
async def refresh_tokens(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db_session),
) -> AuthResponse:
    service = AuthService(db)
    return await service.refresh(refresh_token=payload.refresh_token)


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout",
    description="Revoke the provided refresh token. The access token remains valid until it expires.",
)
async def logout(
    payload: LogoutRequest,
    db: AsyncSession = Depends(get_db_session),
) -> LogoutResponse:
    service = AuthService(db)
    await service.logout(refresh_token=payload.refresh_token)
    return LogoutResponse(detail="Logged out successfully")


@router.get(
    "/me",
    response_model=AuthUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Return the authenticated user's full profile.",
)
async def get_me(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session),
) -> AuthUserResponse:
    result = await db.execute(
        select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    return AuthUserResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        account_state=current_user.account_state,
        email_verified=current_user.email_verified,
        full_name=profile.full_name if profile else None,
        phone=profile.phone if profile else None,
        discord_id=profile.discord_id if profile else None,
        wallet_address=profile.wallet_address if profile else None,
        cohort=profile.cohort if profile else None,
        onboarding_status=profile.onboarding_status if profile else None,
        bio=profile.bio if profile else None,
    )


@router.post(
    "/verify-email",
    response_model=VerifyEmailResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify email with 6-digit code",
    description=(
        "Verify the authenticated user's email address using the "
        "6-digit code sent after account activation. "
        "Code expires after 30 minutes."
    ),
)
async def verify_email(
    payload: VerifyEmailRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session),
) -> VerifyEmailResponse:
    service = AuthService(db)
    return await service.verify_email(user=current_user, code=payload.code)


@router.post(
    "/resend-verification",
    response_model=VerifyEmailResponse,
    status_code=status.HTTP_200_OK,
    summary="Resend email verification code",
    description=(
        "Generate and send a new 6-digit verification code to the "
        "authenticated user's email. Replaces any existing code."
    ),
)
async def resend_verification(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session),
) -> VerifyEmailResponse:
    service = AuthService(db)
    return await service.resend_verification_code(user=current_user)


@router.post(
    "/request-password-reset",
    response_model=PasswordResetResponse,
    status_code=status.HTTP_200_OK,
    summary="Request password reset",
    description=(
        "Request a password reset email for the given address. "
        "If the account exists, an email with a reset link is sent. "
        "Always returns a generic message (to prevent enumeration)."
    ),
)
async def request_password_reset(
    payload: PasswordResetRequest,
    db: AsyncSession = Depends(get_db_session),
) -> PasswordResetResponse:
    service = AuthService(db)
    return await service.request_password_reset(email=payload.email)


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset password",
    description="Reset the account password using a valid password reset token. "
    "All existing refresh tokens are revoked.",
)
async def reset_password(
    payload: PasswordResetConfirmRequest,
    db: AsyncSession = Depends(get_db_session),
) -> MessageResponse:
    service = AuthService(db)
    await service.reset_password(token=payload.token, new_password=payload.new_password)
    return MessageResponse(detail="Password reset successfully")


@router.post(
    "/change-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Change password",
    description="Change the password for the currently authenticated user. "
    "Requires the current password for verification. All existing refresh tokens are revoked.",
)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session),
) -> MessageResponse:
    service = AuthService(db)
    await service.change_password(
        user=current_user,
        current_password=payload.current_password,
        new_password=payload.new_password,
    )
    return MessageResponse(detail="Password changed successfully")
