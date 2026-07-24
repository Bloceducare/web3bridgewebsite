from pydantic import ValidationError

from app.models.portal import AccountState, OnboardingStatus, StudentProfile, User
from app.schemas.students import ArchiveStudentRequest, UpdateStudentRequest
from app.services.students import StudentsService


class DummySession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.commit_count = 0
        self.refreshed: list[object] = []

    def add(self, obj: object) -> None:
        self.added.append(obj)

    async def commit(self) -> None:
        self.commit_count += 1

    async def refresh(self, obj: object) -> None:
        self.refreshed.append(obj)


def build_staff_user() -> User:
    return User(
        id=99,
        email="staff@example.com",
        role="staff",
        account_state=AccountState.ACTIVE.value,
    )


def build_student_user() -> User:
    return User(
        id=5,
        email="student@example.com",
        role="student",
        account_state=AccountState.ACTIVE.value,
    )


def build_student_profile() -> StudentProfile:
    return StudentProfile(
        id=7,
        user_id=5,
        full_name="Student Example",
        phone="08000000000",
        discord_id="student#1234",
        wallet_address="0x123",
        cohort="Cohort XIV",
        onboarding_status=OnboardingStatus.COMPLETED.value,
        bio="Hello world",
    )


async def test_list_students_returns_student_responses() -> None:
    service = StudentsService(DummySession())  # type: ignore[arg-type]
    user = build_student_user()
    profile = build_student_profile()

    async def list_users() -> list[User]:
        return [user]

    async def get_profile(_: int) -> StudentProfile:
        return profile

    service._list_student_users = list_users  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]

    response = await service.list_students()

    assert len(response) == 1
    assert response[0].user_id == user.id
    assert response[0].full_name == profile.full_name


async def test_list_students_filtering_by_cohort() -> None:
    service = StudentsService(DummySession())  # type: ignore[arg-type]
    user = build_student_user()
    profile = build_student_profile()

    async def list_users(cohort: str | None = None) -> list[User]:
        if cohort == "Cohort XIV":
            return [user]
        return []

    async def get_profile(_: int) -> StudentProfile:
        return profile

    service._list_student_users = list_users  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]

    # test matching cohort
    response = await service.list_students(cohort="Cohort XIV")
    assert len(response) == 1
    assert response[0].user_id == user.id

    # test mismatching cohort
    response_empty = await service.list_students(cohort="Cohort XV")
    assert len(response_empty) == 0


async def test_update_student_updates_state_and_profile_and_logs_audit() -> None:
    session = DummySession()
    service = StudentsService(session)  # type: ignore[arg-type]
    actor = build_staff_user()
    user = build_student_user()
    profile = build_student_profile()

    async def get_student(_: int) -> User:
        return user

    async def get_profile(_: int) -> StudentProfile:
        return profile

    service._get_student_by_id = get_student  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]

    response = await service.update_student(
        actor=actor,
        student_id=user.id,
        payload=UpdateStudentRequest(
            full_name="Updated Name",
            cohort="Cohort XV",
            account_state=AccountState.SUSPENDED.value,
            bio="Updated bio",
        ),
    )

    assert user.account_state == AccountState.SUSPENDED.value
    assert profile.full_name == "Updated Name"
    assert profile.cohort == "Cohort XV"
    assert profile.bio == "Updated bio"
    assert response.account_state == AccountState.SUSPENDED.value
    assert response.full_name == "Updated Name"
    assert any(type(obj).__name__ == "StudentStatusHistory" for obj in session.added)
    assert any(type(obj).__name__ == "AuditLog" for obj in session.added)
    assert session.commit_count == 1


async def test_archive_student_deactivates_student_and_logs_audit() -> None:
    session = DummySession()
    service = StudentsService(session)  # type: ignore[arg-type]
    actor = build_staff_user()
    user = build_student_user()
    profile = build_student_profile()

    async def get_student(_: int) -> User:
        return user

    async def get_profile(_: int) -> StudentProfile:
        return profile

    service._get_student_by_id = get_student  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]

    response = await service.archive_student(
        actor=actor,
        student_id=user.id,
        payload=ArchiveStudentRequest(reason="manual_archive"),
    )

    assert user.account_state == AccountState.DEACTIVATED.value
    assert response.account_state == AccountState.DEACTIVATED.value
    assert any(type(obj).__name__ == "StudentStatusHistory" for obj in session.added)
    assert any(type(obj).__name__ == "AuditLog" for obj in session.added)
    assert session.commit_count == 1


def test_update_student_request_rejects_invalid_state_values() -> None:
    try:
        UpdateStudentRequest(account_state="not_a_real_state")
    except ValidationError as exc:
        assert "account_state" in str(exc)
    else:
        raise AssertionError("Expected invalid account_state to fail validation")

    try:
        UpdateStudentRequest(onboarding_status="not_a_real_status")
    except ValidationError as exc:
        assert "onboarding_status" in str(exc)
    else:
        raise AssertionError("Expected invalid onboarding_status to fail validation")
