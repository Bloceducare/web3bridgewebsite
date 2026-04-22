from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import AccountState, StudentProfile, StudentUpdate, User, UserRole
from app.schemas.dashboard import AdminDashboardOverviewResponse, DashboardRecentStudentResponse


class DashboardService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_admin_overview(self) -> AdminDashboardOverviewResponse:
        total_students = await self._count_students()
        active_students = await self._count_students_by_state(AccountState.ACTIVE.value)
        suspended_students = await self._count_students_by_state(AccountState.SUSPENDED.value)
        invited_students = await self._count_students_by_state(AccountState.INVITED.value)
        deactivated_students = await self._count_students_by_state(AccountState.DEACTIVATED.value)
        pending_discord_invites = await self._count_pending_discord_invites()
        published_announcements = await self._count_published_announcements()
        recent_students = await self._list_recent_students()

        return AdminDashboardOverviewResponse(
            total_students=total_students,
            active_students=active_students,
            suspended_students=suspended_students,
            invited_students=invited_students,
            deactivated_students=deactivated_students,
            pending_discord_invites=pending_discord_invites,
            published_announcements=published_announcements,
            recent_students=recent_students,
        )

    async def _count_students(self) -> int:
        result = await self.session.execute(
            select(func.count(User.id)).where(User.role == UserRole.STUDENT.value)
        )
        return int(result.scalar() or 0)

    async def _count_students_by_state(self, state: str) -> int:
        result = await self.session.execute(
            select(func.count(User.id)).where(
                User.role == UserRole.STUDENT.value,
                User.account_state == state,
            )
        )
        return int(result.scalar() or 0)

    async def _count_pending_discord_invites(self) -> int:
        result = await self.session.execute(
            select(func.count(StudentProfile.id)).where(
                StudentProfile.discord_invite_link.is_(None),
            )
        )
        return int(result.scalar() or 0)

    async def _count_published_announcements(self) -> int:
        result = await self.session.execute(
            select(func.count(StudentUpdate.id)).where(StudentUpdate.is_published.is_(True))
        )
        return int(result.scalar() or 0)

    async def _list_recent_students(self) -> list[DashboardRecentStudentResponse]:
        result = await self.session.execute(
            select(User, StudentProfile)
            .outerjoin(StudentProfile, StudentProfile.user_id == User.id)
            .where(User.role == UserRole.STUDENT.value)
            .order_by(User.created_at.desc())
            .limit(8)
        )
        rows = result.all()
        return [
            DashboardRecentStudentResponse(
                user_id=user.id,
                full_name=profile.full_name if profile else None,
                email=user.email,
                cohort=profile.cohort if profile else None,
                account_state=user.account_state,
                created_at=user.created_at,
            )
            for user, profile in rows
        ]
