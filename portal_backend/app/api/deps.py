import secrets
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import TokenType, decode_token
from app.db.session import get_db_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import AccountState, Mentor, User, UserRole
from app.services.auth import AuthService

bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    description="Paste your JWT access token from POST /api/v1/auth/login",
)
http_bearer_optional = HTTPBearer(auto_error=False)
automation_api_key_header = APIKeyHeader(name="API-Key", auto_error=False)
settings = get_settings()


@dataclass(frozen=True, slots=True)
class AutomationAuth:
    user: User | None
    via_api_key: bool


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    payload = decode_token(credentials.credentials, expected_type=TokenType.ACCESS)
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


async def get_current_mentor_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    if current_user.role != UserRole.MENTOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Mentor access required",
        )
    result = await db.execute(
        select(Mentor).where(Mentor.user_id == current_user.id, Mentor.is_active.is_(True))
    )
    mentor = result.scalar_one_or_none()
    if mentor is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Active mentor profile required",
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


def _is_valid_automation_api_key(api_key: str) -> bool:
    expected = settings.effective_automation_api_key
    if not api_key or not expected:
        return False
    return secrets.compare_digest(api_key, expected)


async def get_active_user_or_automation_api_key(
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer_optional),
    api_key: str | None = Depends(automation_api_key_header),
    db: AsyncSession = Depends(get_db_session),
) -> AutomationAuth:
    if api_key is not None:
        if not _is_valid_automation_api_key(api_key):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API key",
            )
        return AutomationAuth(user=None, via_api_key=True)

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = decode_token(credentials.credentials, expected_type=TokenType.ACCESS)
    service = AuthService(db)
    user = await service.get_user_by_id(int(payload["sub"]))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.account_state != AccountState.ACTIVE.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is not active")
    return AutomationAuth(user=user, via_api_key=False)
