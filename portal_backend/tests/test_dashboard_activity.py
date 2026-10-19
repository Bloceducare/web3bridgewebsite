from datetime import datetime, UTC
from app.models.portal import AuditLog, Mentor, User, UserRole
from app.services.dashboard import DashboardService

from datetime import datetime, UTC
from app.models.portal import Attendance, AttendanceCode, AuditLog, Mentor, StudentProfile, User, UserRole
from app.services.dashboard import DashboardService

class DummyResult:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows

    def scalars(self):
        class Scalars:
            def __init__(self, rows):
                self._rows = rows
            def all(self):
                return self._rows
        return Scalars(self._rows)

class MultiDummySession:
    def __init__(self, responses: dict) -> None:
        self.responses = responses

    async def execute(self, statement: any, params: any = None) -> any:
        stmt_str = str(statement)
        for key, rows in self.responses.items():
            if key in stmt_str:
                return DummyResult(rows)
        return DummyResult([])

class DummySession:
    def __init__(self, rows) -> None:
        self.rows = rows

    async def execute(self, statement: any, params: any = None) -> any:
        return DummyResult(self.rows)

async def test_list_recent_mentor_activity() -> None:
    user = User(id=10, email="mentor@example.com", role=UserRole.MENTOR.value)
    mentor = Mentor(id=1, user_id=10, full_name="Olayiwola", programme="Web3 Solidity", track="Web3")
    audit = AuditLog(id=100, actor_user_id=10, action="course_material_created", resource_type="course_material", resource_id="5", created_at=datetime.now(UTC))

    session = DummySession(rows=[(audit, user, mentor)])
    service = DashboardService(session)  # type: ignore[arg-type]

    activities = await service.list_recent_mentor_activity()
    assert len(activities) == 1
    assert activities[0].actor_name == "Olayiwola"
    assert activities[0].description == "Olayiwola the mentor for Web3 Solidity (Web3) just uploaded a course material"

async def test_attendance_group_activity_multiple_students() -> None:
    now = datetime.now(UTC)
    mentor = Mentor(id=1, user_id=10, full_name="Olayiwola", programme="Web3 Solidity", track="Web3")
    code = AttendanceCode(
        id=5,
        code="W3B99",
        programme="Web3 Solidity",
        track="Web3",
        duration=30,
        expires_at=now,
        is_active=True,
        mentor_id=1,
        created_at=now,
    )
    code.mentor = mentor
    attendances = [
        Attendance(id=1, attendance_code_id=5, student_name="Amiola", date=now.strftime("%Y-%m-%d"), time="12:01:00", created_at=now)
    ]
    for i in range(2, 19):
        attendances.append(
            Attendance(id=i, attendance_code_id=5, student_name=f"Student {i}", date=now.strftime("%Y-%m-%d"), time="12:05:00", created_at=now)
        )
    code.attendances = attendances

    session = MultiDummySession(responses={"attendance_codes": [code], "audit_logs": []})
    service = DashboardService(session)  # type: ignore[arg-type]

    activities = await service.list_recent_activity()
    # Should have student attendance group and mentor created attendance
    signed_group = next(a for a in activities if a.action == "attendance_signed_group")
    assert signed_group.actor_name == "Amiola"
    assert signed_group.description == "Amiola and 17 others in class signed attendance today"

    mentor_created = next(a for a in activities if a.action == "attendance_code_created")
    assert "Olayiwola created attendance" in mentor_created.description
    assert "today" in mentor_created.description

async def test_attendance_group_activity_single_student() -> None:
    now = datetime.now(UTC)
    mentor = Mentor(id=1, user_id=10, full_name="Olayiwola", programme="Web3 Solidity", track="Web3")
    code = AttendanceCode(
        id=6,
        code="W3B88",
        programme="Web3 Solidity",
        track="Web3",
        duration=30,
        expires_at=now,
        is_active=True,
        mentor_id=1,
        created_at=now,
    )
    code.mentor = mentor
    code.attendances = [
        Attendance(id=1, attendance_code_id=6, student_name="Amiola", date=now.strftime("%Y-%m-%d"), time="12:01:00", created_at=now)
    ]

    session = MultiDummySession(responses={"attendance_codes": [code], "audit_logs": []})
    service = DashboardService(session)  # type: ignore[arg-type]

    activities = await service.list_recent_activity()
    signed_group = next(a for a in activities if a.action == "attendance_signed_group")
    assert signed_group.description == "Amiola in class signed attendance today"

async def test_recent_activity_announcement_and_assessment() -> None:
    now = datetime.now(UTC)
    user = User(id=20, email="student@example.com", role=UserRole.STUDENT.value)
    profile = StudentProfile(id=1, user_id=20, full_name="Amiola", programme="Web3 Solidity", track="Web3")

    audit_assessment = AuditLog(
        id=101,
        actor_user_id=20,
        action="assessment_submitted",
        resource_type="assessment_result",
        resource_id="12",
        after_json={"title": "Solidity Basics Assessment", "score": 95},
        created_at=now,
    )

    mentor_user = User(id=10, email="mentor@example.com", role=UserRole.MENTOR.value)
    mentor = Mentor(id=1, user_id=10, full_name="Olayiwola", programme="Web3 Solidity", track="Web3")
    audit_update = AuditLog(
        id=102,
        actor_user_id=10,
        action="student_update_created",
        resource_type="student_update",
        resource_id="3",
        after_json={"title": "Final Project Guidelines"},
        created_at=now,
    )

    session = MultiDummySession(
        responses={
            "attendance_codes": [],
            "audit_logs": [
                (audit_assessment, user, None, profile),
                (audit_update, mentor_user, mentor, None),
            ],
        }
    )
    service = DashboardService(session)  # type: ignore[arg-type]

    activities = await service.list_recent_activity()
    assert len(activities) == 2
    assessment_act = next(a for a in activities if a.action == "assessment_submitted")
    assert assessment_act.description == 'Amiola submitted assessment: "Solidity Basics Assessment"'

    update_act = next(a for a in activities if a.action == "student_update_created")
    assert update_act.description == 'Olayiwola posted an announcement: "Final Project Guidelines"'

