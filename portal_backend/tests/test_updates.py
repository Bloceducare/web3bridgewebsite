from datetime import UTC, datetime

from app.models.portal import (
    StudentProfile,
    StudentUpdate,
    StudentUpdateRead,
    UpdateTargetType,
    User,
)
from app.schemas.updates import CreateStudentUpdateRequest, UpdateStudentUpdateRequest
from app.services.updates import UpdatesService


class DummySession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.commit_count = 0
        self.refresh_count = 0
        self.flush_count = 0
        self.deleted: list[object] = []

    def add(self, obj: object) -> None:
        if getattr(obj, "id", None) is None and type(obj).__name__ == "StudentUpdate":
            obj.id = 101
        self.added.append(obj)

    async def commit(self) -> None:
        self.commit_count += 1

    async def refresh(self, obj: object) -> None:
        self.refresh_count += 1

    async def flush(self) -> None:
        self.flush_count += 1

    async def delete(self, obj: object) -> None:
        self.deleted.append(obj)


def build_staff_user() -> User:
    return User(id=1, email="staff@example.com", role="staff", account_state="active")


def build_student_user() -> User:
    return User(id=2, email="student@example.com", role="student", account_state="active")


def build_update(**overrides: object) -> StudentUpdate:
    return StudentUpdate(
        id=overrides.get("id", 11),
        title=overrides.get("title", "Portal notice"),
        body=overrides.get("body", "Important update"),
        target_type=overrides.get("target_type", UpdateTargetType.ALL_ACTIVE.value),
        target_ref=overrides.get("target_ref", None),
        is_published=overrides.get("is_published", True),
        send_in_app=overrides.get("send_in_app", True),
        send_email=overrides.get("send_email", False),
        published_at=overrides.get("published_at", datetime.now(UTC)),
        created_by=overrides.get("created_by", 1),
        created_at=overrides.get("created_at", datetime.now(UTC)),
        updated_at=overrides.get("updated_at", datetime.now(UTC)),
    )


async def test_create_update_creates_audited_published_update() -> None:
    session = DummySession()
    service = UpdatesService(session)  # type: ignore[arg-type]

    response = await service.create_update(
        actor=build_staff_user(),
        payload=CreateStudentUpdateRequest(
            title="Launch day",
            body="Portal is live",
            target_type=UpdateTargetType.ALL_ACTIVE,
            is_published=True,
        ),
    )

    assert response.id == 101
    assert response.title == "Launch day"
    assert response.is_published is True
    assert response.send_in_app is True
    assert response.send_email is False
    assert response.published_at is not None
    assert any(type(obj).__name__ == "AuditLog" for obj in session.added)
    assert session.commit_count == 1


async def test_list_my_updates_filters_visible_updates() -> None:
    session = DummySession()
    service = UpdatesService(session)  # type: ignore[arg-type]
    user = build_student_user()
    profile = StudentProfile(user_id=user.id, full_name="Student", cohort="Cohort XIV")
    matching = build_update(
        id=1, target_type=UpdateTargetType.COHORT.value, target_ref="Cohort XIV"
    )
    individual = build_update(
        id=2, target_type=UpdateTargetType.INDIVIDUAL.value, target_ref=str(user.id)
    )
    hidden = build_update(id=3, target_type=UpdateTargetType.COHORT.value, target_ref="Cohort XV")

    async def list_published() -> list[StudentUpdate]:
        return [matching, individual, hidden]

    async def get_profile(_: int) -> StudentProfile:
        return profile

    async def get_read_record(*, update_id: int, user_id: int) -> StudentUpdateRead | None:
        if update_id == 2 and user_id == user.id:
            return StudentUpdateRead(update_id=2, user_id=user.id, read_at=datetime.now(UTC))
        return None

    service._list_published_updates = list_published  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]
    service._get_read_record = get_read_record  # type: ignore[method-assign]

    response = await service.list_my_updates(user=user)

    assert [item.id for item in response] == [1, 2]
    assert response[0].read_at is None
    assert response[1].read_at is not None


async def test_mark_update_as_read_creates_read_record_once() -> None:
    session = DummySession()
    service = UpdatesService(session)  # type: ignore[arg-type]
    user = build_student_user()
    profile = StudentProfile(user_id=user.id, full_name="Student", cohort="Cohort XIV")
    student_update = build_update(id=20, target_type=UpdateTargetType.ALL_ACTIVE.value)

    async def get_profile(_: int) -> StudentProfile:
        return profile

    async def get_update(_: int) -> StudentUpdate:
        return student_update

    async def get_read_record(*, update_id: int, user_id: int) -> StudentUpdateRead | None:
        return None

    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]
    service._get_update_by_id = get_update  # type: ignore[method-assign]
    service._get_read_record = get_read_record  # type: ignore[method-assign]

    response = await service.mark_update_as_read(user=user, update_id=20)

    assert response.detail == "Update marked as read"
    assert any(type(obj).__name__ == "StudentUpdateRead" for obj in session.added)
    assert session.commit_count == 1


async def test_update_update_updates_publish_state() -> None:
    session = DummySession()
    service = UpdatesService(session)  # type: ignore[arg-type]
    student_update = build_update(is_published=False, published_at=None)

    async def get_update(_: int) -> StudentUpdate:
        return student_update

    service._get_update_by_id = get_update  # type: ignore[method-assign]

    response = await service.update_update(
        actor=build_staff_user(),
        update_id=student_update.id,
        payload=UpdateStudentUpdateRequest(is_published=True, title="Updated title"),
    )

    assert response.is_published is True
    assert response.title == "Updated title"
    assert response.published_at is not None
    assert any(type(obj).__name__ == "AuditLog" for obj in session.added)


async def test_delete_update_deletes_and_audits() -> None:
    session = DummySession()
    service = UpdatesService(session)  # type: ignore[arg-type]
    student_update = build_update(id=50)

    async def get_update(_: int) -> StudentUpdate:
        return student_update

    service._get_update_by_id = get_update  # type: ignore[method-assign]

    response = await service.delete_update(actor=build_staff_user(), update_id=50)

    assert response.detail == "Update deleted successfully"
    assert session.deleted == [student_update]
    assert any(type(obj).__name__ == "AuditLog" for obj in session.added)
