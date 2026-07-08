from app.models.portal import (
    AccountState,
    ExternalStudentMap,
    OnboardingStatus,
    StudentProfile,
    User,
)
from app.schemas.onboarding import OnboardingInviteRequest
from app.services.onboarding import OnboardingService


def test_is_zk_course_detects_zk_names() -> None:
    assert OnboardingService.is_zk_course("ZK Cohort XIV") is True
    assert OnboardingService.is_zk_course("Zero Knowledge Bootcamp") is True
    assert OnboardingService.is_zk_course("Web3 Cohort XIV") is False
    assert OnboardingService.is_zk_course("Rust Masterclass") is False


def test_build_activation_url_includes_token_query() -> None:
    activation_url = OnboardingService.build_activation_url("sample-token")

    assert "/activate?" in activation_url
    assert "token=sample-token" in activation_url


def test_normalize_approval_status_aliases() -> None:
    assert OnboardingService.normalize_approval_status("accepted") == "approved"
    assert OnboardingService.normalize_approval_status("APPROVED") == "approved"
    assert OnboardingService.normalize_approval_status("declined") == "rejected"
    assert OnboardingService.normalize_approval_status("suspended") == "revoked"
    assert OnboardingService.normalize_approval_status("in_review") == "pending"
    assert OnboardingService.normalize_approval_status(None) == "pending"


class DummySession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.commit_count = 0
        self.refreshed: list[object] = []

    def add(self, obj: object) -> None:
        self.added.append(obj)

    async def flush(self) -> None:
        return None

    async def commit(self) -> None:
        self.commit_count += 1

    async def refresh(self, obj: object) -> None:
        self.refreshed.append(obj)


def build_payload() -> OnboardingInviteRequest:
    return OnboardingInviteRequest(
        email="student@example.com",
        full_name="Student Example",
        cohort="Cohort XIV",
        course_name="Web3 Cohort XIV",
        external_student_id="external-1",
        source_system="backend_v2",
        source_email="student@example.com",
        approval_status="approved",
    )


async def test_invite_non_zk_student_keeps_active_users_active() -> None:
    session = DummySession()
    service = OnboardingService(session)  # type: ignore[arg-type]
    payload = build_payload()

    user = User(
        id=1,
        email="student@example.com",
        role="student",
        account_state=AccountState.ACTIVE.value,
    )
    profile = StudentProfile(
        user_id=1,
        full_name="Existing Student",
        cohort="Old Cohort",
        onboarding_status=OnboardingStatus.COMPLETED.value,
    )
    external_map = ExternalStudentMap(
        user_id=1,
        source_system="backend_v2",
        external_student_id="external-1",
        source_email="student@example.com",
        approval_status="approved",
    )

    async def get_user(_: str) -> User:
        return user

    async def get_profile(_: int) -> StudentProfile:
        return profile

    async def get_external_map(_: str) -> ExternalStudentMap:
        return external_map

    async def unexpected_activation(*, user: User) -> str:
        raise AssertionError(f"activation token should not be created for active user {user.id}")

    service._get_user_by_email = get_user  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]
    service._get_external_map = get_external_map  # type: ignore[method-assign]
    service.auth_service.create_activation_token_for_user = unexpected_activation  # type: ignore[method-assign]

    response = await service.invite_non_zk_student(payload=payload)

    assert user.account_state == AccountState.ACTIVE.value
    assert response.account_state == AccountState.ACTIVE.value
    assert response.activation_url is None
    assert response.portal_invite_created is False
    assert response.reason == "portal_invite_skipped_active_account"
    assert profile.onboarding_status == OnboardingStatus.COMPLETED.value
    assert not any(type(obj).__name__ == "StudentStatusHistory" for obj in session.added)


async def test_invite_non_zk_student_resends_for_invited_users() -> None:
    session = DummySession()
    service = OnboardingService(session)  # type: ignore[arg-type]
    payload = build_payload()

    user = User(
        id=2,
        email="student@example.com",
        role="student",
        account_state=AccountState.INVITED.value,
    )
    profile = StudentProfile(
        user_id=2,
        full_name="Existing Student",
        cohort="Old Cohort",
        onboarding_status=OnboardingStatus.PENDING.value,
    )
    external_map = ExternalStudentMap(
        user_id=2,
        source_system="backend_v2",
        external_student_id="external-1",
        source_email="student@example.com",
        approval_status="approved",
    )

    async def get_user(_: str) -> User:
        return user

    async def get_profile(_: int) -> StudentProfile:
        return profile

    async def get_external_map(_: str) -> ExternalStudentMap:
        return external_map

    async def create_activation(*, user: User) -> str:
        assert user.id == 2
        return "invite-token"

    service._get_user_by_email = get_user  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]
    service._get_external_map = get_external_map  # type: ignore[method-assign]
    service.auth_service.create_activation_token_for_user = create_activation  # type: ignore[method-assign]

    response = await service.invite_non_zk_student(payload=payload)

    assert user.account_state == AccountState.INVITED.value
    assert response.account_state == AccountState.INVITED.value
    assert response.activation_url == OnboardingService.build_activation_url("invite-token")
    assert response.reason == "portal_invite_resent"
    assert profile.onboarding_status == OnboardingStatus.INVITED.value


async def test_invite_non_zk_student_normalizes_approval_status() -> None:
    session = DummySession()
    service = OnboardingService(session)  # type: ignore[arg-type]
    payload = build_payload()
    payload.approval_status = "accepted"

    user = User(
        id=3,
        email="student@example.com",
        role="student",
        account_state=AccountState.INVITED.value,
    )
    profile = StudentProfile(
        user_id=3,
        full_name="Existing Student",
        cohort="Old Cohort",
        onboarding_status=OnboardingStatus.PENDING.value,
    )
    external_map = ExternalStudentMap(
        user_id=3,
        source_system="backend_v2",
        external_student_id="external-1",
        source_email="student@example.com",
        approval_status="pending",
    )

    async def get_user(_: str) -> User:
        return user

    async def get_profile(_: int) -> StudentProfile:
        return profile

    async def get_external_map(_: str) -> ExternalStudentMap:
        return external_map

    async def create_activation(*, user: User) -> str:
        return "invite-token"

    service._get_user_by_email = get_user  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]
    service._get_external_map = get_external_map  # type: ignore[method-assign]
    service.auth_service.create_activation_token_for_user = create_activation  # type: ignore[method-assign]

    await service.invite_non_zk_student(payload=payload)

    assert external_map.approval_status == "approved"


def test_apply_backend_participant_row_overrides_request_fields() -> None:
    payload = build_payload()
    payload.course_name = "Wrong Course"
    payload.cohort = "Wrong Cohort"
    payload.full_name = "Wrong Name"

    updated = OnboardingService._apply_backend_participant_row(
        payload,
        {
            "participant_id": 99,
            "email": "student@example.com",
            "full_name": "DB Student",
            "cohort": "Cohort XIV",
            "registration_cohort": "Reg Cohort",
            "source_status": "ACCEPTED",
            "payment_status": True,
            "course_name": "Web3 Cohort XIV",
        },
    )

    assert updated.full_name == "DB Student"
    assert updated.cohort == "Cohort XIV"
    assert updated.course_name == "Web3 Cohort XIV"
    assert updated.external_student_id == "99"


async def test_invite_non_zk_student_rejects_unpaid_backend_participant() -> None:
    from fastapi import HTTPException

    session = DummySession()
    service = OnboardingService(session)  # type: ignore[arg-type]
    payload = build_payload()

    async def load_unpaid(_external_student_id: str) -> dict:
        return {
            "participant_id": 1,
            "email": "student@example.com",
            "full_name": "Student",
            "cohort": "Cohort XIV",
            "source_status": "ACCEPTED",
            "payment_status": False,
            "course_name": "Web3 Cohort XIV",
        }

    service._load_backend_v2_participant = load_unpaid  # type: ignore[method-assign]

    try:
        await service.invite_non_zk_student(payload=payload)
        raise AssertionError("expected HTTPException")
    except HTTPException as exc:
        assert exc.status_code == 400
        assert "payment" in str(exc.detail).lower()


async def test_invite_zk_student_requires_approval() -> None:
    from fastapi import HTTPException

    session = DummySession()
    service = OnboardingService(session)  # type: ignore[arg-type]
    payload = OnboardingInviteRequest(
        email="zk@example.com",
        full_name="ZK Student",
        cohort="Master Class III",
        course_name="ZK Engineering: Cryptography, Circuits & Protocols",
        external_student_id="99",
        source_system="backend_v2",
        approval_status="pending",
    )

    async def load_pending_zk(_external_student_id: str) -> dict:
        return {
            "participant_id": 99,
            "email": "zk@example.com",
            "full_name": "ZK Student",
            "cohort": "Master Class III",
            "source_status": "PENDING",
            "payment_status": True,
            "course_name": "ZK Engineering: Cryptography, Circuits & Protocols",
        }

    service._load_backend_v2_participant = load_pending_zk  # type: ignore[method-assign]

    try:
        await service.invite_non_zk_student(payload=payload)
        raise AssertionError("expected HTTPException")
    except HTTPException as exc:
        assert exc.status_code == 400
        assert "approved" in str(exc.detail).lower()


async def test_invite_zk_student_succeeds_when_approved() -> None:
    session = DummySession()
    service = OnboardingService(session)  # type: ignore[arg-type]
    payload = OnboardingInviteRequest(
        email="zk@example.com",
        full_name="ZK Student",
        cohort="Master Class III",
        course_name="ZK Engineering: Cryptography, Circuits & Protocols",
        external_student_id="99",
        source_system="backend_v2",
        approval_status="accepted",
    )

    async def load_approved_zk(_external_student_id: str) -> dict:
        return {
            "participant_id": 99,
            "email": "zk@example.com",
            "full_name": "ZK Student",
            "cohort": "Master Class III",
            "source_status": "ACCEPTED",
            "payment_status": True,
            "course_name": "ZK Engineering: Cryptography, Circuits & Protocols",
        }

    async def get_user(_: str) -> User | None:
        return None

    async def get_profile(_: int) -> StudentProfile | None:
        return None

    async def get_external_map(_: str) -> ExternalStudentMap | None:
        return None

    async def create_activation(*, user: User) -> str:
        return "zk-token"

    service._load_backend_v2_participant = load_approved_zk  # type: ignore[method-assign]
    service._get_user_by_email = get_user  # type: ignore[method-assign]
    service._get_profile_by_user_id = get_profile  # type: ignore[method-assign]
    service._get_external_map = get_external_map  # type: ignore[method-assign]
    service.auth_service.create_activation_token_for_user = create_activation  # type: ignore[method-assign]

    response = await service.invite_non_zk_student(payload=payload)

    assert response.portal_invite_created is True
    assert response.reason == "portal_invite_created"
    assert response.activation_url == OnboardingService.build_activation_url("zk-token")
