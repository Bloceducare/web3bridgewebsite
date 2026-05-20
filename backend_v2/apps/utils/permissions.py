import base64
import json

import requests
from django.conf import settings
from rest_framework import permissions

from .exceptions.requests import JWTException, RequestException

_ALLOWED_ADMIN_ROLES = frozenset(
    {
        "admin",
        "general_admin",
        "system_admin",
        "staff",
    }
)
_DENIED_ROLES = frozenset({"student", "mentor"})


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


def _truthy(value) -> bool:
    if value is True:
        return True
    if value is False or value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def _iter_profile_dicts(payload: dict):
    if not isinstance(payload, dict):
        return
    yield payload
    for key in ("user", "data", "profile", "payload"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            yield nested


def _role_from_blob(blob: dict) -> str:
    return _normalize_role(
        blob.get("role")
        or blob.get("user_role")
        or blob.get("user_type")
        or blob.get("account_type")
    )


def _blob_grants_admin(blob: dict) -> bool | None:
    """
    Return True/False if this blob clearly grants or denies admin; None if inconclusive.
    """
    if _truthy(blob.get("is_admin")) or _truthy(blob.get("is_staff")):
        return True
    if _truthy(blob.get("is_superuser")):
        return True
    if _truthy(blob.get("is_student")):
        return False

    role = _role_from_blob(blob)
    if role in _ALLOWED_ADMIN_ROLES:
        return True
    if role in _DENIED_ROLES:
        return False

    groups = blob.get("groups") or blob.get("roles") or []
    if isinstance(groups, str):
        groups = [groups]
    if isinstance(groups, list):
        for group in groups:
            gnorm = _normalize_role(str(group))
            if gnorm in _ALLOWED_ADMIN_ROLES or "admin" in gnorm:
                return True

    return None


def _jwt_claims_unverified(raw_token: str) -> dict:
    try:
        parts = (raw_token or "").split(".")
        if len(parts) < 2:
            return {}
        segment = parts[1]
        padding = "=" * (-len(segment) % 4)
        decoded = base64.urlsafe_b64decode(segment + padding)
        payload = json.loads(decoded.decode("utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _is_admin_user(payload: dict, raw_token: str = "") -> bool:
    """
    Auth server verify JSON and JWT claims may each carry admin signals.
    """
    sources: list[dict] = []
    if isinstance(payload, dict):
        sources.extend(_iter_profile_dicts(payload))
    claims = _jwt_claims_unverified(raw_token)
    if claims:
        sources.extend(_iter_profile_dicts(claims))

    for blob in sources:
        if _blob_grants_admin(blob) is True:
            return True

    return False


def _verify_token_with_auth_server(raw_token: str) -> dict | None:
    url = settings.AUTH_SERVER_URL + "/api/token/verify/"
    try:
        response = requests.post(url, json={"token": raw_token}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, dict) else {}
        if response.status_code in (401, 403):
            return None
    except Exception as exc:
        raise RequestException(str(exc)) from exc

    for auth_value in (f"Bearer {raw_token}", raw_token):
        try:
            response = requests.post(
                url, headers={"Authorization": auth_value}, timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, dict) else {}
        except Exception:
            continue
    return None


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
            payload = _verify_token_with_auth_server(raw_token)
            if payload is None:
                raise RequestException("Error authenticating from auth server")

            if _is_admin_user(payload, raw_token=raw_token):
                return True
            return False

        except (JWTException, RequestException):
            raise
        except Exception as exc:
            raise RequestException(str(exc)) from exc
