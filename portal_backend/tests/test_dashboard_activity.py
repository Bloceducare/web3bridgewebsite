from datetime import datetime, UTC
from app.models.portal import AuditLog, Mentor, User, UserRole
from app.services.dashboard import DashboardService

class DummySession:
    def __init__(self, rows) -> None:
        self.rows = rows

    async def execute(self, statement: any, params: any = None) -> any:
        class Result:
            def __init__(self, rows):
                self.rows = rows
            def all(self):
                return self.rows
        return Result(self.rows)

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
