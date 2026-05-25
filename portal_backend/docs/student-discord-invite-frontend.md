# Student Discord invite — frontend quick reference

```http
POST /api/v1/me/discord-invite
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "discord_email": "student.discord@gmail.com"
}
```

## Response `200`

```json
{
  "invite_url": "https://discord.gg/xxxxx",
  "invite_code": "xxxxx",
  "discord_email": "student.discord@gmail.com",
  "replaced_previous_invite": false,
  "message": "Discord invite created"
}
```

## Rules

| Case | Behavior |
|------|----------|
| First request | Creates invite, saves `discord_email` on profile |
| Same `discord_email` again | Returns existing `invite_url` (no new invite) |
| **Different** `discord_email` | Revokes old invite, creates new one (`replaced_previous_invite: true`) |
| Another student’s Discord email | `409` conflict |

Students can **only** generate for themselves (token identity). No `user_id` in body.

`GET /api/v1/me/profile` includes `discord_email`, `discord_invite_link` after success.

## Errors

| Code | Meaning |
|------|---------|
| `401` | Not logged in |
| `403` | Not a student / email not verified |
| `409` | Discord email used by another account |
| `503` | Portal missing `DISCORD_BOT_API_KEY` or discord-bot down |

## Ops env (portal_backend)

```env
DISCORD_BOT_API_URL=https://dreadful-addia-web3bridge-84cd21c2.koyeb.app
DISCORD_BOT_API_KEY=<same as API_KEY on discord-bot service>
DISCORD_STUDENT_ROLE=cohort-xv
DISCORD_INVITE_CATEGORY_ID=<optional category snowflake>
```

Do not call portal `admin/discord/*` from the student app — portal proxies to discord-bot for this flow.
