from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

pytest.importorskip("asyncpg")

from app.api import deps
from app.db.session import get_db_session
from app.main import app
from app.models.portal import AccountState, User
from app.schemas.courses import (
    AdminCourseSummaryResponse,
    StudentCourseResponse,
    StudentGuarantorFormResponse,
)
from app.schemas.dashboard import AdminDashboardOverviewResponse, DashboardRecentStudentResponse
from app.schemas.discord import (
    DiscordInviteGenerateResponse,
    PendingDiscordInviteStudentResponse,
)
from app.schemas.notifications import (
    MarkNotificationReadResponse,
    NotificationItemResponse,
    NotificationSummaryResponse,
)
from app.schemas.mentor import MentorStudentResponse
from app.schemas.updates import StudentUpdateResponse
from app.services.courses import CoursesService
from app.services.mentor import MentorPortalService
from app.services.dashboard import DashboardService
from app.services.discord import DiscordService
from app.services.notifications import NotificationsService
from app.services.portal_management import PortalManagementService
from app.services.students import StudentsService
from app.services.updates import UpdatesService

client = TestClient(app)


class DummyDBSession:
    pass


async def override_db_session() -> AsyncGenerator[DummyDBSession, None]:
    yield DummyDBSession()


def build_user(*, user_id: int, role: str, account_state: str = AccountState.ACTIVE.value) -> User:
    return User(
        id=user_id,
        email=f"{role}{user_id}@example.com",
        role=role,
        account_state=account_state,
        email_verified=True,
    )


def clear_overrides() -> None:
    app.dependency_overrides.clear()


def test_notifications_my_returns_items() -> None:
    current_user = build_user(user_id=10, role="student")

    async def override_verified_user() -> User:
        return current_user

    async def list_my_notifications(
        _: NotificationsService,
        *,
        user: User,
    ) -> list[NotificationItemResponse]:
        return [
            NotificationItemResponse(
                id=1,
                title="Welcome",
                body="Hello student",
                is_read=False,
                read_at=None,
                published_at=datetime.now(UTC),
                created_at=datetime.now(UTC),
            )
        ]

    original_method = NotificationsService.list_my_notifications
    NotificationsService.list_my_notifications = list_my_notifications
    app.dependency_overrides[deps.get_current_verified_user] = override_verified_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/notifications/my")
    finally:
        NotificationsService.list_my_notifications = original_method
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["title"] == "Welcome"
    assert payload[0]["is_read"] is False


def test_notifications_summary_returns_counts() -> None:
    current_user = build_user(user_id=11, role="student")

    async def override_verified_user() -> User:
        return current_user

    async def get_my_summary(
        _: NotificationsService,
        *,
        user: User,
    ) -> NotificationSummaryResponse:
        return NotificationSummaryResponse(total=8, unread=3)

    original_method = NotificationsService.get_my_summary
    NotificationsService.get_my_summary = get_my_summary
    app.dependency_overrides[deps.get_current_verified_user] = override_verified_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/notifications/my/summary")
    finally:
        NotificationsService.get_my_summary = original_method
        clear_overrides()

    assert response.status_code == 200
    assert response.json() == {"total": 8, "unread": 3}


def test_notifications_mark_read_returns_timestamp() -> None:
    current_user = build_user(user_id=12, role="student")

    async def override_verified_user() -> User:
        return current_user

    async def mark_as_read(
        _: NotificationsService,
        *,
        user: User,
        notification_id: int,
    ) -> MarkNotificationReadResponse:
        assert notification_id == 15
        return MarkNotificationReadResponse(detail="Notification marked as read", read_at=datetime.now(UTC))

    original_method = NotificationsService.mark_as_read
    NotificationsService.mark_as_read = mark_as_read
    app.dependency_overrides[deps.get_current_verified_user] = override_verified_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post("/api/v1/notifications/15/read")
    finally:
        NotificationsService.mark_as_read = original_method
        clear_overrides()

    assert response.status_code == 200
    assert response.json()["detail"] == "Notification marked as read"


def test_dashboard_overview_requires_staff_or_admin() -> None:
    current_user = build_user(user_id=21, role="student")

    async def override_active_user() -> User:
        return current_user

    app.dependency_overrides[deps.get_current_active_user] = override_active_user
    try:
        response = client.get("/api/v1/admin/dashboard/overview")
    finally:
        clear_overrides()

    assert response.status_code == 403
    assert response.json()["detail"] == "Staff or admin access required"


def test_dashboard_overview_returns_metrics() -> None:
    current_user = build_user(user_id=22, role="staff")

    async def override_staff_user() -> User:
        return current_user

    async def get_admin_overview(_: DashboardService) -> AdminDashboardOverviewResponse:
        return AdminDashboardOverviewResponse(
            total_students=100,
            active_students=80,
            suspended_students=5,
            invited_students=10,
            deactivated_students=5,
            pending_discord_invites=12,
            published_announcements=7,
            recent_students=[
                DashboardRecentStudentResponse(
                    user_id=1,
                    full_name="Recent Student",
                    email="recent@example.com",
                    cohort="Cohort XIV",
                    account_state="active",
                    created_at=datetime.now(UTC),
                )
            ],
        )

    original_method = DashboardService.get_admin_overview
    DashboardService.get_admin_overview = get_admin_overview
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_staff_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/admin/dashboard/overview")
    finally:
        DashboardService.get_admin_overview = original_method
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_students"] == 100
    assert payload["recent_students"][0]["email"] == "recent@example.com"


def test_courses_my_returns_courses_for_student() -> None:
    current_user = build_user(user_id=30, role="student")

    async def override_verified_user() -> User:
        return current_user

    async def list_my_courses(_: CoursesService, *, user: User) -> list[StudentCourseResponse]:
        return [
            StudentCourseResponse(
                course_id=1,
                course_name="Solidity Basics",
                cohort="Cohort XIV",
                approval_status="ACCEPTED",
                payment_status=True,
                source_updated_at=datetime.now(UTC),
            )
        ]

    original_method = CoursesService.list_my_courses
    CoursesService.list_my_courses = list_my_courses
    app.dependency_overrides[deps.get_current_verified_user] = override_verified_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/courses/my")
    finally:
        CoursesService.list_my_courses = original_method
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["course_name"] == "Solidity Basics"


def test_courses_my_guarantor_form_returns_published_form() -> None:
    current_user = build_user(user_id=32, role="student")

    async def override_verified_user() -> User:
        return current_user

    async def get_my_published_guarantor_form(
        _: CoursesService, *, user: User
    ) -> StudentGuarantorFormResponse:
        assert user.id == current_user.id
        return StudentGuarantorFormResponse(
            id=3,
            title="Cohort XIV Guarantor Form",
            form_url="https://forms.example.com/guarantor",
            cohort="Cohort XIV",
            is_active=True,
        )

    original_method = CoursesService.get_my_published_guarantor_form
    CoursesService.get_my_published_guarantor_form = get_my_published_guarantor_form
    app.dependency_overrides[deps.get_current_verified_user] = override_verified_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/courses/my/guarantor-form")
    finally:
        CoursesService.get_my_published_guarantor_form = original_method
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 3
    assert payload["is_active"] is True


def test_courses_my_guarantor_form_returns_404_when_not_available() -> None:
    current_user = build_user(user_id=33, role="student")

    async def override_verified_user() -> User:
        return current_user

    async def get_my_published_guarantor_form(_: CoursesService, *, user: User):
        assert user.id == current_user.id
        raise HTTPException(
            status_code=404, detail="No published guarantor form is available yet"
        )

    original_method = CoursesService.get_my_published_guarantor_form
    CoursesService.get_my_published_guarantor_form = get_my_published_guarantor_form
    app.dependency_overrides[deps.get_current_verified_user] = override_verified_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/courses/my/guarantor-form")
    finally:
        CoursesService.get_my_published_guarantor_form = original_method
        clear_overrides()

    assert response.status_code == 404
    assert response.json()["detail"] == "No published guarantor form is available yet"


def test_courses_admin_summary_returns_aggregates() -> None:
    current_user = build_user(user_id=31, role="admin")

    async def override_admin_user() -> User:
        return current_user

    async def list_admin_course_summaries(_: CoursesService) -> list[AdminCourseSummaryResponse]:
        return [
            AdminCourseSummaryResponse(
                course_id=1,
                course_name="Solidity Basics",
                total_students=40,
                accepted_students=32,
                paid_students=29,
            )
        ]

    original_method = CoursesService.list_admin_course_summaries
    CoursesService.list_admin_course_summaries = list_admin_course_summaries
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_admin_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/courses/admin/summary")
    finally:
        CoursesService.list_admin_course_summaries = original_method
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["paid_students"] == 29


def test_discord_pending_invites_requires_internal_auth() -> None:
    response = client.get("/api/v1/admin/discord/invites/pending")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid internal API key"


def test_discord_pending_invites_returns_students() -> None:
    async def override_internal_key() -> str:
        return "ok"

    async def list_pending_invites(
        _: DiscordService,
        *,
        limit: int,
    ) -> list[PendingDiscordInviteStudentResponse]:
        assert limit == 25
        return [
            PendingDiscordInviteStudentResponse(
                user_id=9,
                full_name="Invite Pending",
                email="pending@example.com",
                cohort="Cohort XIV",
                discord_email=None,
                onboarding_status="invited",
            )
        ]

    original_method = DiscordService.list_pending_invites
    DiscordService.list_pending_invites = list_pending_invites
    app.dependency_overrides[deps.verify_internal_api_key] = override_internal_key
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/admin/discord/invites/pending?limit=25")
    finally:
        DiscordService.list_pending_invites = original_method
        clear_overrides()

    assert response.status_code == 200
    assert response.json()[0]["email"] == "pending@example.com"


def test_discord_generate_invite_stores_record() -> None:
    async def override_internal_key() -> str:
        return "ok"

    async def upsert_generated_invite(
        _: DiscordService,
        *,
        payload: object,
    ) -> DiscordInviteGenerateResponse:
        return DiscordInviteGenerateResponse(
            detail="Discord invite stored",
            user_id=8,
            invite_link="https://discord.gg/example",
            updated_at=datetime.now(UTC),
        )

    original_method = DiscordService.upsert_generated_invite
    DiscordService.upsert_generated_invite = upsert_generated_invite
    app.dependency_overrides[deps.verify_internal_api_key] = override_internal_key
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/admin/discord/invites/generate",
            json={
                "user_id": 8,
                "invite_link": "https://discord.gg/example",
                "discord_id": "123456",
                "discord_email": "user@example.com",
            },
        )
    finally:
        DiscordService.upsert_generated_invite = original_method
        clear_overrides()

    assert response.status_code == 200
    assert response.json()["detail"] == "Discord invite stored"


def test_updates_create_accepts_delivery_channel_fields() -> None:
    current_user = build_user(user_id=40, role="staff")

    async def override_staff_user() -> User:
        return current_user

    async def create_update(
        _: UpdatesService,
        *,
        actor: User,
        payload: object,
    ) -> StudentUpdateResponse:
        return StudentUpdateResponse(
            id=101,
            title="Email + In-app",
            body="Important announcement",
            target_type="all_active",
            target_ref=None,
            is_published=True,
            send_in_app=True,
            send_email=True,
            published_at=datetime.now(UTC),
            created_by=actor.id,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            read_at=None,
        )

    original_method = UpdatesService.create_update
    UpdatesService.create_update = create_update
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_staff_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/updates",
            json={
                "title": "Email + In-app",
                "body": "Important announcement",
                "target_type": "all_active",
                "is_published": True,
                "send_in_app": True,
                "send_email": True,
            },
        )
    finally:
        UpdatesService.create_update = original_method
        clear_overrides()

    assert response.status_code == 201
    payload = response.json()
    assert payload["send_in_app"] is True
    assert payload["send_email"] is True


def test_updates_create_rejects_when_no_channel_selected() -> None:
    current_user = build_user(user_id=41, role="staff")

    async def override_staff_user() -> User:
        return current_user

    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_staff_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/updates",
            json={
                "title": "Invalid channels",
                "body": "Should fail",
                "target_type": "all_active",
                "is_published": True,
                "send_in_app": False,
                "send_email": False,
            },
        )
    finally:
        clear_overrides()

    assert response.status_code == 422
    assert "At least one delivery channel must be enabled" in response.json()["detail"]


def test_notifications_admin_announcement_endpoint_creates_update() -> None:
    current_user = build_user(user_id=51, role="staff")

    async def override_staff_user() -> User:
        return current_user

    async def create_update(
        _: UpdatesService,
        *,
        actor: User,
        payload: object,
    ) -> StudentUpdateResponse:
        assert actor.id == current_user.id
        assert getattr(payload, "target_type").value == "all_active"
        return StudentUpdateResponse(
            id=500,
            title="Platform Notice",
            body="Scheduled maintenance",
            target_type="all_active",
            target_ref=None,
            is_published=True,
            send_in_app=True,
            send_email=False,
            published_at=datetime.now(UTC),
            created_by=actor.id,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            read_at=None,
        )

    original_method = UpdatesService.create_update
    UpdatesService.create_update = create_update
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_staff_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.post(
            "/api/v1/notifications/admin/announcements",
            json={
                "title": "Platform Notice",
                "body": "Scheduled maintenance",
                "scope": "platform",
                "sender_type": "general_admin",
                "is_published": True,
                "send_in_app": True,
                "send_email": False,
            },
        )
    finally:
        UpdatesService.create_update = original_method
        clear_overrides()

    assert response.status_code == 201
    assert response.json()["update_id"] == 500


def test_students_evict_endpoint_calls_service() -> None:
    current_user = build_user(user_id=52, role="admin")

    async def override_admin_user() -> User:
        return current_user

    async def evict_student(
        _: StudentsService,
        *,
        actor: User,
        student_id: int,
        reason: str | None = None,
    ):
        assert actor.id == current_user.id
        assert student_id == 90
        from app.schemas.students import StudentResponse

        return StudentResponse(
            user_id=90,
            email="evicted@example.com",
            role="student",
            account_state="suspended",
            full_name="Evicted Student",
            cohort="Cohort XIV",
        )

    original_method = StudentsService.evict_student
    StudentsService.evict_student = evict_student
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_admin_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.post("/api/v1/students/90/evict", json={"reason": "violation"})
    finally:
        StudentsService.evict_student = original_method
        clear_overrides()

    assert response.status_code == 200
    assert response.json()["account_state"] == "suspended"


def test_portal_materials_returns_structured_payload() -> None:
    current_user = build_user(user_id=53, role="staff")

    async def override_staff_user() -> User:
        return current_user

    async def list_course_materials(
        _: PortalManagementService, *, course_id: int | None = None
    ):
        assert course_id == 7
        from app.schemas.portal_management import CourseMaterialResponse

        return [
            CourseMaterialResponse(
                id=1,
                course_id=7,
                title="Week 1 Recording",
                material_type="video",
                resource_url="https://example.com/video",
                content=None,
                metadata={"duration": "35m"},
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
        ]

    original_method = PortalManagementService.list_course_materials
    PortalManagementService.list_course_materials = list_course_materials
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_staff_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.get("/api/v1/admin/portal/materials?course_id=7")
    finally:
        PortalManagementService.list_course_materials = original_method
        clear_overrides()

    assert response.status_code == 200
    assert response.json()[0]["material"]["type"] == "video"


def test_invite_student_by_email_requires_staff_or_admin() -> None:
    current_user = build_user(user_id=60, role="student")

    async def override_current_user() -> User:
        return current_user

    app.dependency_overrides[deps.get_current_user] = override_current_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.post(
            "/api/v1/admin/portal/users/invite/student",
            json={"email": "newstudent@example.com"},
        )
    finally:
        clear_overrides()

    assert response.status_code == 403


def test_invite_student_by_email_success_for_general_admin() -> None:
    from app.schemas.onboarding import OnboardingInviteResponse

    general_admin = build_user(user_id=62, role="general_admin")

    async def override_staff_or_admin() -> User:
        return general_admin

    async def invite_student_by_email(_self, *, actor: User, email: str) -> OnboardingInviteResponse:
        assert actor.id == general_admin.id
        return OnboardingInviteResponse(
            user_id=101,
            email=email,
            account_state="invited",
            onboarding_status="invited",
            activation_url="https://frontend.example/activate/onboard?token=y",
            portal_invite_created=True,
            reason="portal_invite_created",
        )

    original = PortalManagementService.invite_student_by_email
    PortalManagementService.invite_student_by_email = invite_student_by_email
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_staff_or_admin
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.post(
            "/api/v1/admin/portal/users/invite/student",
            json={"email": "generaladmin-student@example.com"},
        )
    finally:
        PortalManagementService.invite_student_by_email = original
        clear_overrides()

    assert response.status_code == 200
    assert response.json()["email"] == "generaladmin-student@example.com"


def test_invite_student_by_email_success_for_admin() -> None:
    from app.schemas.onboarding import OnboardingInviteResponse

    admin = build_user(user_id=61, role="system_admin")

    async def override_current_admin() -> User:
        return admin

    async def invite_student_by_email(_self, *, actor: User, email: str) -> OnboardingInviteResponse:
        assert actor.id == admin.id
        assert email == "newstudent@example.com"
        return OnboardingInviteResponse(
            user_id=100,
            email=email,
            account_state="invited",
            onboarding_status="invited",
            activation_url="https://frontend.example/activate/onboard?token=x",
            portal_invite_created=True,
            reason="portal_invite_created",
        )

    original = PortalManagementService.invite_student_by_email
    PortalManagementService.invite_student_by_email = invite_student_by_email
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = override_current_admin
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.post(
            "/api/v1/admin/portal/users/invite/student",
            json={"email": "newstudent@example.com"},
        )
    finally:
        PortalManagementService.invite_student_by_email = original
        clear_overrides()

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == 100
    assert body["email"] == "newstudent@example.com"
    assert body["portal_invite_created"] is True


def test_mentor_course_summary_requires_mentor_role() -> None:
    staff = build_user(user_id=70, role="staff")
    app.dependency_overrides[deps.get_current_staff_or_admin_user] = lambda: staff
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.get("/api/v1/mentor/courses/summary")
    finally:
        clear_overrides()
    assert response.status_code == 403


def test_mentor_course_summary_returns_assigned_summaries() -> None:
    mentor_user = build_user(user_id=71, role="mentor")

    async def override_mentor_user() -> User:
        return mentor_user

    async def list_course_summaries(
        _: MentorPortalService, *, actor: User
    ) -> list[AdminCourseSummaryResponse]:
        assert actor.id == mentor_user.id
        return [
            AdminCourseSummaryResponse(
                course_id=5,
                course_name="Web3 Basics",
                total_students=20,
                accepted_students=18,
                paid_students=15,
            )
        ]

    original = MentorPortalService.list_course_summaries
    MentorPortalService.list_course_summaries = list_course_summaries
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.get("/api/v1/mentor/courses/summary")
    finally:
        MentorPortalService.list_course_summaries = original
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["course_id"] == 5


def test_mentor_create_update_broadcasts_to_course() -> None:
    mentor_user = build_user(user_id=72, role="mentor")

    async def override_mentor_user() -> User:
        return mentor_user

    async def create_course_update(
        _: MentorPortalService, *, actor: User, payload: object
    ) -> StudentUpdateResponse:
        assert actor.id == mentor_user.id
        assert getattr(payload, "course_id") == 5
        return StudentUpdateResponse(
            id=200,
            title="Week 1",
            body="Read chapter 1",
            target_type="course",
            target_ref="5",
            is_published=True,
            send_in_app=True,
            send_email=False,
            published_at=datetime.now(UTC),
            created_by=actor.id,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            read_at=None,
        )

    original = MentorPortalService.create_course_update
    MentorPortalService.create_course_update = create_course_update
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.post(
            "/api/v1/mentor/updates",
            json={
                "course_id": 5,
                "title": "Week 1",
                "body": "Read chapter 1",
                "is_published": True,
            },
        )
    finally:
        MentorPortalService.create_course_update = original
        clear_overrides()

    assert response.status_code == 201
    assert response.json()["target_type"] == "course"


def test_mentor_list_updates_returns_course_announcements() -> None:
    mentor_user = build_user(user_id=75, role="mentor")

    async def override_mentor_user() -> User:
        return mentor_user

    async def list_course_updates(
        _: MentorPortalService, *, actor: User, course_id: int | None
    ) -> list[StudentUpdateResponse]:
        assert actor.id == mentor_user.id
        assert course_id == 5
        return [
            StudentUpdateResponse(
                id=201,
                title="Week 2",
                body="Complete assignment",
                target_type="course",
                target_ref="5",
                is_published=True,
                send_in_app=True,
                send_email=False,
                published_at=datetime.now(UTC),
                created_by=actor.id,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                read_at=None,
            )
        ]

    original = MentorPortalService.list_course_updates
    MentorPortalService.list_course_updates = list_course_updates
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.get("/api/v1/mentor/updates?course_id=5")
    finally:
        MentorPortalService.list_course_updates = original
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["title"] == "Week 2"


def test_mentor_course_materials_by_course_id() -> None:
    mentor_user = build_user(user_id=76, role="mentor")

    async def override_mentor_user() -> User:
        return mentor_user

    class _MaterialRow:
        def __init__(self) -> None:
            self.id = 1
            self.course_id = 5
            self.title = "Intro slides"
            self.material_type = "link"
            self.resource_url = "https://example.com/slides"
            self.content = None
            self.metadata_json = {"week": 1}

    async def list_materials(
        _: MentorPortalService, *, actor: User, course_id: int | None
    ) -> list[_MaterialRow]:
        assert actor.id == mentor_user.id
        assert course_id == 5
        return [_MaterialRow()]

    original = MentorPortalService.list_materials
    MentorPortalService.list_materials = list_materials
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.get("/api/v1/courses/5/materials")
    finally:
        MentorPortalService.list_materials = original
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["course_id"] == 5
    assert payload[0]["title"] == "Intro slides"


def test_mentor_students_list_returns_enrollments() -> None:
    mentor_user = build_user(user_id=73, role="mentor")

    async def override_mentor_user() -> User:
        return mentor_user

    async def list_students(
        _: MentorPortalService, *, actor: User, course_id: int | None
    ) -> list[MentorStudentResponse]:
        assert actor.id == mentor_user.id
        assert course_id == 5
        return [
            MentorStudentResponse(
                participant_name="Ada Lovelace",
                email="ada@example.com",
                course_id=5,
                course_name="Web3 Basics",
                cohort="Cohort XIV",
                approval_status="ACCEPTED",
                payment_status=True,
                portal_user_id=10,
                account_state="active",
                source_updated_at=datetime.now(UTC),
            )
        ]

    original = MentorPortalService.list_students
    MentorPortalService.list_students = list_students
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.get("/api/v1/mentor/students?course_id=5")
    finally:
        MentorPortalService.list_students = original
        clear_overrides()

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["email"] == "ada@example.com"


def test_invite_portal_user_rejects_course_id_for_non_mentor() -> None:
    admin = build_user(user_id=74, role="system_admin")

    async def override_current_admin() -> User:
        return admin

    app.dependency_overrides[deps.get_current_admin_user] = override_current_admin
    app.dependency_overrides[get_db_session] = override_db_session
    try:
        response = client.post(
            "/api/v1/admin/portal/users/invite",
            json={
                "email": "admin2@example.com",
                "full_name": "General Admin",
                "role": "general_admin",
                "course_id": 3,
            },
        )
    finally:
        clear_overrides()

    assert response.status_code == 422
