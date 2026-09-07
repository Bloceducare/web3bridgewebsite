from typing import Any

SUBMISSION_GRACE_SECONDS = 120


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace(" ", "_")


def question_field(question: dict[str, Any], *names: str) -> Any:
    normalized = {_normalize_key(k): v for k, v in question.items()}
    for name in names:
        value = normalized.get(_normalize_key(name))
        if value is not None:
            return value
    return None


def question_quiz_id(question: dict[str, Any]) -> str | None:
    raw = question_field(question, "Quiz_ID", "quiz_id")
    if raw is None:
        return None
    text = str(raw).strip()
    return text or None


def question_assessment_id(question: dict[str, Any]) -> str | None:
    raw = question_field(question, "Assessment_ID", "assessment_id")
    if raw is None:
        return None
    text = str(raw).strip()
    return text or None


def question_has_answer_key(question: dict[str, Any]) -> bool:
    answer = question_field(question, "Answer", "answer")
    if answer is None:
        return False
    return str(answer).strip() != ""


def normalize_answer(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().upper()


def strip_answer_from_question(question: dict[str, Any]) -> dict[str, Any]:
    blocked = {"answer", "explanation"}
    return {
        key: value
        for key, value in question.items()
        if _normalize_key(key) not in blocked
    }


def questions_for_student(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [strip_answer_from_question(item) for item in questions]


def breakdown_for_student_view(
    breakdown: list[dict[str, Any]],
    *,
    result_release_mode: str,
    result_status: str,
) -> list[dict[str, Any]]:
    """Remove answer keys from grading breakdown returned to students."""
    show_correct = result_status == "graded" or (
        result_release_mode == "immediate"
        and result_status in {"submitted", "graded"}
    )
    sanitized: list[dict[str, Any]] = []
    for item in breakdown:
        row = dict(item)
        row.pop("expected", None)
        if not show_correct:
            row["correct"] = None
        sanitized.append(row)
    return sanitized


def serialize_questions(questions: list[Any]) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []
    for item in questions:
        if hasattr(item, "model_dump"):
            serialized.append(item.model_dump())
        elif isinstance(item, dict):
            serialized.append(dict(item))
        else:
            serialized.append(dict(item))
    return serialized


def build_answer_lookup(answers: list[dict[str, Any]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for index, item in enumerate(answers):
        answer = item.get("answer")
        if answer is None:
            continue
        quiz_id = item.get("quiz_id") or item.get("Quiz_ID")
        assessment_id = item.get("assessment_id") or item.get("Assessment_ID")
        if quiz_id is not None:
            lookup[f"quiz:{str(quiz_id).strip()}"] = str(answer)
        if assessment_id is not None:
            lookup[f"assessment:{str(assessment_id).strip()}"] = str(answer)
        lookup[f"index:{index}"] = str(answer)
    return lookup


def resolve_student_answer(
    question: dict[str, Any],
    *,
    index: int,
    lookup: dict[str, str],
) -> str | None:
    quiz_id = question_quiz_id(question)
    if quiz_id is not None:
        value = lookup.get(f"quiz:{quiz_id}")
        if value is not None:
            return value
    assessment_id = question_assessment_id(question)
    if assessment_id is not None:
        value = lookup.get(f"assessment:{assessment_id}")
        if value is not None:
            return value
    return lookup.get(f"index:{index}")


def auto_grade_submission(
    questions: list[dict[str, Any]],
    answers: list[dict[str, Any]],
) -> tuple[int, list[dict[str, Any]]]:
    lookup = build_answer_lookup(answers)
    breakdown: list[dict[str, Any]] = []
    score = 0

    for index, question in enumerate(questions):
        quiz_id = question_quiz_id(question)
        assessment_id = question_assessment_id(question)
        given = resolve_student_answer(question, index=index, lookup=lookup)
        expected_raw = question_field(question, "Answer", "answer")
        auto_graded = question_has_answer_key(question)
        correct: bool | None = None

        if auto_graded and expected_raw is not None:
            correct = normalize_answer(given) == normalize_answer(expected_raw)
            if correct:
                score += 1

        breakdown.append(
            {
                "quiz_id": quiz_id,
                "assessment_id": assessment_id,
                "correct": correct,
                "expected": str(expected_raw) if expected_raw is not None else None,
                "given": given,
                "auto_graded": auto_graded and correct is not None,
                "mentor_override": False,
            }
        )

    return score, breakdown
