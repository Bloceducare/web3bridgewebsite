from app.clients.discord_bot import extract_discord_invite_code
from app.services.student_discord import StudentDiscordService


def test_extract_discord_invite_code_from_gg_link() -> None:
    assert extract_discord_invite_code("https://discord.gg/AbCdEfGh") == "AbCdEfGh"


def test_extract_discord_invite_code_from_invite_path() -> None:
    assert (
        extract_discord_invite_code("https://discord.com/invite/xyz123")
        == "xyz123"
    )


def test_extract_discord_invite_code_returns_none_for_empty() -> None:
    assert extract_discord_invite_code(None) is None
    assert extract_discord_invite_code("") is None
