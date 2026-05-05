from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import TokenType, decode_token
from app.db.session import get_db_session
from app.models.portal import AccountState, User, UserRole
from app.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
settings = get_settings()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    payload = decode_token(token, expected_type=TokenType.ACCESS)
    service = AuthService(db)
    user = await service.get_user_by_id(int(payload["sub"]))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.account_state != AccountState.ACTIVE.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is not active")
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please verify your email to continue.",
        )
    return current_user


async def get_current_staff_or_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role not in {
        UserRole.STAFF.value,
        UserRole.ADMIN.value,
        UserRole.GENERAL_ADMIN.value,
        UserRole.SYSTEM_ADMIN.value,
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff or admin access required",
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role not in {UserRole.ADMIN.value, UserRole.SYSTEM_ADMIN.value}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


async def verify_internal_api_key(
    x_internal_api_key: str = Header(default="", alias="X-Internal-API-Key"),
) -> str:
    if not x_internal_api_key or x_internal_api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid internal API key"
        )
    return x_internal_api_key
