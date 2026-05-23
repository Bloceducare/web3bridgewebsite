from datetime import UTC, datetime, timedelta

from app.services.assessment_grading import (
    SUBMISSION_GRACE_SECONDS,
    auto_grade_submission,
    breakdown_for_student_view,
    questions_for_student,
    strip_answer_from_question,
)


def test_strip_answer_from_question() -> None:
    question = {
        "Quiz_ID": "q1",
        "Question": "What is 2+2?",
        "Options": {"A": "3", "B": "4"},
        "Answer": "B",
        "Explanation": "2+2 is 4",
    }
    stripped = strip_answer_from_question(question)
    assert "Answer" not in stripped
    assert "Explanation" not in stripped
    assert stripped["Quiz_ID"] == "q1"


def test_questions_for_student_removes_all_answers() -> None:
    questions = [
        {"Quiz_ID": "1", "Question": "Q1", "Answer": "A"},
        {"quiz_id": "2", "question": "Q2", "answer": "true"},
    ]
    student_view = questions_for_student(questions)
    assert all("Answer" not in q and "answer" not in q for q in student_view)


def test_auto_grade_multiple_choice() -> None:
    questions = [
        {
            "Quiz_ID": "1",
            "Question": "Pick one",
            "Options": {"A": "wrong", "B": "right"},
            "Answer": "B",
            "Type": "multiple_choice",
        },
        {
            "Quiz_ID": "2",
            "Question": "Explain",
            "Type": "open_ended",
        },
    ]
    answers = [
        {"quiz_id": "1", "answer": "b"},
        {"quiz_id": "2", "answer": "Because"},
    ]
    score, breakdown = auto_grade_submission(questions, answers)
    assert score == 1
    assert breakdown[0]["correct"] is True
    assert breakdown[0]["auto_graded"] is True
    assert breakdown[1]["correct"] is None
    assert breakdown[1]["auto_graded"] is False


def test_breakdown_for_student_view_strips_expected() -> None:
    breakdown = [
        {
            "quiz_id": "1",
            "correct": True,
            "expected": "B",
            "given": "B",
            "auto_graded": True,
        }
    ]
    sanitized = breakdown_for_student_view(
        breakdown,
        result_release_mode="immediate",
        result_status="graded",
    )
    assert "expected" not in sanitized[0]
    assert sanitized[0]["correct"] is True


def test_breakdown_for_student_view_hides_correct_until_release() -> None:
    breakdown = [{"quiz_id": "1", "correct": True, "expected": "B", "given": "A"}]
    sanitized = breakdown_for_student_view(
        breakdown,
        result_release_mode="mentor_controlled",
        result_status="submitted",
    )
    assert sanitized[0].get("correct") is None
    assert "expected" not in sanitized[0]


def test_grace_window_is_two_minutes() -> None:
    started = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    expires = started + timedelta(minutes=30, seconds=SUBMISSION_GRACE_SECONDS)
    assert expires == started + timedelta(minutes=32)
