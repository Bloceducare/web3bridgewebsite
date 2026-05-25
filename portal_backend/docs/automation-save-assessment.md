# n8n / automation — save mentor assessment

## Correct request

```http
PUT https://<host>/api/v1/admin/portal/mentor-assessments/{mentor_assessment_id}/save
API-Key: <AUTOMATION_API_KEY>
Content-Type: application/json
```

**Common mistake:** missing `/api/v1` in the URL.

Wrong: `https://host/admin/portal/mentor-assessments/12/save`  
Right: `https://host/api/v1/admin/portal/mentor-assessments/12/save`

## Example body

```json
{
  "title": "Week 3 Quiz",
  "duration_minutes": 60,
  "due_at": "2026-05-30T23:59:59+00:00",
  "questions": [
    {
      "Quiz_ID": "q1",
      "Question": "What is 2+2?",
      "Options": { "A": "3", "B": "4", "C": "5", "D": "6" },
      "Answer": "B",
      "Type": "multiple_choice"
    }
  ],
  "assessment_type": "multiple_choice",
  "evaluation_mode": "ai",
  "result_release_mode": "immediate",
  "accepted": true
}
```

### Enum values

| Field | Allowed |
|--------|---------|
| `assessment_type` | `multiple_choice`, `open_ended`, `combined` |
| `evaluation_mode` | `ai`, `manual` |
| `result_release_mode` | `immediate`, `mentor_controlled` |

`accepted` must be JSON boolean (`true` / `false`), not a quoted string.

## n8n HTTP Request node

| Setting | Value |
|---------|--------|
| Method | PUT |
| URL | `https://<host>/api/v1/admin/portal/mentor-assessments/{{ $json.Mentor_Assessment_ID }}/save` |
| Header `API-Key` | value from env |
| Header `Content-Type` | `application/json` |
| Body | JSON (see above) |

## Responses

| Code | Meaning |
|------|---------|
| `200` | Saved |
| `401` | Wrong/missing `API-Key` |
| `404` | `mentor_assessment_id` not found |
| `422` | Invalid body (bad enums, missing `questions`, etc.) |
| `503` | DB/migration issue |

## Deploy checklist (Koyeb)

1. Set `AUTOMATION_API_KEY` in service env (or rely on `PAYMENT_API_KEY` fallback).
2. Run Alembic migrations on the DB (`portal.mentor_assessments`, etc.).
3. Redeploy after code changes.
