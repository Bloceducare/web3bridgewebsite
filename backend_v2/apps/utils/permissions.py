from rest_framework import permissions
import requests
from django.conf import settings
from .exceptions.requests import RequestException, JWTException

_ALLOWED_ADMIN_ROLES = frozenset(
    {
        "admin",
        "general_admin",
        "system_admin",
        "staff",
    }
)


def _extract_bearer_token(authorization_header: str) -> str:
    """Return the raw JWT from an Authorization header value."""
    value = (authorization_header or "").strip()
    if not value:
        return ""
    parts = value.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1].strip()
    return value


def _normalize_role(raw_role: str | None) -> str:
    return (raw_role or "").strip().lower().replace(" ", "_").replace("-", "_")


def _is_admin_user(payload: dict) -> bool:
    """Auth server may return admin flags on the root object or under ``user``."""
    if not isinstance(payload, dict):
        return False

    user_blob = payload.get("user")
    if not isinstance(user_blob, dict):
        user_blob = payload

    if payload.get("is_admin") or user_blob.get("is_admin"):
        return True

    role = _normalize_role(user_blob.get("role") or payload.get("role"))
    return role in _ALLOWED_ADMIN_ROLES


class IsAuthenticatedByAuthServer(permissions.BasePermission):
    """
    Custom permission to allow access only to authenticated users
    whose credentials are validated by the authentication server.
    """

    def has_permission(self, request, view):
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise JWTException("Authentication token not provided")

        raw_token = _extract_bearer_token(authorization)
        if not raw_token:
            raise JWTException("Authentication token not provided")

        try:
            response = requests.post(
                settings.AUTH_SERVER_URL + "/api/token/verify/",
                json={"token": raw_token},
                timeout=10,
            )

            if response.status_code != 200:
                raise RequestException("Error authenticating from auth server")

            payload = response.json()
            if _is_admin_user(payload):
                return True
            return False

        except (JWTException, RequestException):
            raise
        except Exception as exc:
            raise RequestException(str(exc)) from exc
