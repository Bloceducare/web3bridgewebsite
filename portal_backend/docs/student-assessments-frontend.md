# Student assessments — frontend quick reference

Base URL: `/api/v1`  
Auth: `Authorization: Bearer <access_token>` (from `POST /api/v1/auth/login`)

Student must be **verified** (`email_verified`) for assessment routes.

---

## Flow

1. **List** published assessments → `GET /mentor-assessments/my`
2. **Start** attempt (get questions) → `POST /mentor-assessments/{id}/start`
3. **Submit** answers → `POST /mentor-assessments/{id}/submit`
4. **Optional:** view result → `GET /assessment-results/{result_id}`

List does **not** include questions or answer keys. Questions only come from **start**.

---

## Status values (`status` on list / submit / result)

| Value | Meaning |
|--------|---------|
| `not_started` | Never started |
| `in_progress` | Started, timer running |
| `submitted` | Submitted, awaiting mentor grade (if needed) |
| `graded` | Final score available |

Use `can_start` and `is_overdue` on the list for UI buttons.

---

## 1. List assessments

```http
GET /api/v1/mentor-assessments/my
GET /api/v1/mentor-assessments/my?course_id=5
```

**Response:** `200` — array of objects:

```json
[
  {
    "mentor_assessment_id": 12,
    "course_id": 5,
    "title": "Week 3 Quiz",
    "assessment_type": "multiple_choice",
    "duration_minutes": 60,
    "due_at": "2026-05-30T23:59:59Z",
    "total_questions": 10,
    "released_at": "2026-05-20T10:00:00Z",
    "result_id": 88,
    "status": "not_started",
    "score": null,
    "max_score": 10,
    "started_at": null,
    "expires_at": null,
    "submitted_at": null,
    "can_start": true,
    "is_overdue": false
  }
]
```

- `score` is `null` until results are released (see below).
- Only assessments for the student’s enrolled courses (same source as `GET /courses/my`).

---

## 2. Start assessment

```http
POST /api/v1/mentor-assessments/12/start
```

**Response:** `200`

```json
{
  "result_id": 88,
  "mentor_assessment_id": 12,
  "started_at": "2026-05-23T12:00:00Z",
  "expires_at": "2026-05-23T13:02:00Z",
  "duration_minutes": 60,
  "questions": [
    {
      "Quiz_ID": "q1",
      "Question": "What is 2+2?",
      "Options": { "A": "3", "B": "4", "C": "5", "D": "6" },
      "Type": "multiple_choice"
    }
  ]
}
```

- Questions **never** include `Answer`, `answer`, or `Explanation`.
- `expires_at` = start time + `duration_minutes` + **2 min grace** for submit.
- Call start again while `in_progress` and not expired → same session (resume).
- Errors: `403` (past due / expired), `409` (already submitted).

---

## 3. Submit answers

```http
POST /api/v1/mentor-assessments/12/submit
Content-Type: application/json

{
  "answers": [
    { "quiz_id": "q1", "answer": "B" },
    { "assessment_id": "alt-id", "answer": "some text" }
  ]
}
```

Each answer item: at least one of `quiz_id` or `assessment_id` (match question IDs), plus `answer` string.

**Response:** `200`

```json
{
  "result_id": 88,
  "mentor_assessment_id": 12,
  "score": 8,
  "max_score": 10,
  "status": "graded",
  "submitted_at": "2026-05-23T12:45:00Z",
  "breakdown": [
    {
      "quiz_id": "q1",
      "assessment_id": null,
      "correct": true,
      "given": "B",
      "auto_graded": true,
      "mentor_override": false
    }
  ]
}
```

**Student breakdown rules:**

- No `expected` field (correct answer key is never sent).
- `correct` only when results are released (`immediate` after submit, or `mentor_controlled` after `graded`).

---

## 4. Get result detail

```http
GET /api/v1/assessment-results/88
```

**Response:** `200` — same shape as submit plus:

```json
{
  "id": 88,
  "mentor_assessment_id": 12,
  "user_id": 42,
  "score": 8,
  "max_score": 10,
  "status": "graded",
  "started_at": "...",
  "expires_at": "...",
  "submitted_at": "...",
  "responses": { "answers": [ { "quiz_id": "q1", "answer": "B" } ] },
  "breakdown": [ ... ]
}
```

Students only see their own `result_id`. Same sanitization as submit breakdown.

---

## Score visibility (list + result)

| `result_release_mode` | When student sees `score` / `correct` |
|------------------------|----------------------------------------|
| `immediate` | After submit (auto-graded items) |
| `mentor_controlled` | After status is `graded` |

---

## Related

```http
GET /api/v1/courses/my
```

Returns `course_id` values you can pass to `?course_id=` on the list endpoint.

---

## Errors (usual)

| Code | Meaning |
|------|---------|
| `401` | Missing/invalid token |
| `403` | Not a student, unverified, past due, or not your result |
| `404` | Assessment not published |
| `409` | Already submitted |
| `422` | Validation (body/query) |

Full OpenAPI: `/docs` on the portal API host.

---

## Discord invite (students)

See [`student-discord-invite-frontend.md`](student-discord-invite-frontend.md).
