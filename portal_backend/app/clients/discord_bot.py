from __future__ import annotations

from typing import Any

import httpx

from app.core.config import get_settings

settings = get_settings()

# Discord gateway can take up to ~60s on cold start before creating an invite.
_DISCORD_BOT_TIMEOUT = httpx.Timeout(90.0, connect=10.0)


class DiscordBotError(Exception):
    def __init__(self, *, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class DiscordBotClient:
    def __init__(self) -> None:
        self.base = settings.DISCORD_BOT_API_URL.rstrip("/")
        self.headers = {
            "X-API-Key": settings.DISCORD_BOT_API_KEY,
            "Content-Type": "application/json",
        }

    async def get_invite_by_email(self, *, email: str) -> dict[str, Any] | None:
        try:
            async with httpx.AsyncClient(timeout=_DISCORD_BOT_TIMEOUT) as client:
                response = await client.get(
                    f"{self.base}/api/v1/invites",
                    params={"email": email},
                    headers=self.headers,
                )
        except httpx.TimeoutException as exc:
            raise DiscordBotError(
                status_code=503,
                detail="Discord invite service timed out. Please try again.",
            ) from exc
        except httpx.HTTPError as exc:
            raise DiscordBotError(
                status_code=503,
                detail="Discord invite service is unreachable. Please try again later.",
            ) from exc
        if response.status_code == 404:
            return None
        if response.status_code >= 400:
            raise self._error_from_response(response)
        payload = response.json()
        if not payload:
            return None
        if isinstance(payload, list):
            return payload[0] if payload else None
        return payload

    async def create_invite(
        self,
        *,
        email: str,
        user_id: int,
        role: str,
        category_id: str | None = None,
        max_uses: int = 1,
        max_age: int = 604800,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "email": email,
            "user_id": user_id,
            "role": role,
            "max_uses": max_uses,
            "max_age": max_age,
        }
        if category_id:
            body["category_id"] = category_id
        try:
            async with httpx.AsyncClient(timeout=_DISCORD_BOT_TIMEOUT) as client:
                response = await client.post(
                    f"{self.base}/api/v1/invites",
                    json=body,
                    headers=self.headers,
                )
        except httpx.TimeoutException as exc:
            raise DiscordBotError(
                status_code=503,
                detail="Discord invite service timed out. Please try again.",
            ) from exc
        except httpx.HTTPError as exc:
            raise DiscordBotError(
                status_code=503,
                detail="Discord invite service is unreachable. Please try again later.",
            ) from exc
        if response.status_code >= 400:
            raise self._error_from_response(response)
        return response.json()

    async def revoke_invite(self, *, invite_code: str) -> dict[str, Any] | None:
        try:
            async with httpx.AsyncClient(timeout=_DISCORD_BOT_TIMEOUT) as client:
                response = await client.delete(
                    f"{self.base}/api/v1/invites/{invite_code}",
                    headers=self.headers,
                )
        except httpx.TimeoutException as exc:
            raise DiscordBotError(
                status_code=503,
                detail="Discord invite service timed out. Please try again.",
            ) from exc
        except httpx.HTTPError as exc:
            raise DiscordBotError(
                status_code=503,
                detail="Discord invite service is unreachable. Please try again later.",
            ) from exc
        if response.status_code in {200, 204, 404}:
            if response.content:
                return response.json()
            return None
        raise self._error_from_response(response)

    @staticmethod
    def _error_from_response(response: httpx.Response) -> DiscordBotError:
        detail = response.text
        try:
            payload = response.json()
            if isinstance(payload, dict) and payload.get("detail"):
                detail = str(payload["detail"])
        except ValueError:
            pass
        return DiscordBotError(status_code=response.status_code, detail=detail)


def extract_discord_invite_code(invite_link: str | None) -> str | None:
    if not invite_link:
        return None
    link = invite_link.strip().rstrip("/")
    if not link:
        return None
    code = link.rsplit("/", 1)[-1]
    return code or None
