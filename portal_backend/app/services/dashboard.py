from datetime import UTC, datetime
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.portal import (
    AccountState,
    Attendance,
    AttendanceCode,
    AuditLog,
    Mentor,
    StudentProfile,
    StudentUpdate,
    User,
    UserRole,
)
from app.schemas.dashboard import AdminDashboardOverviewResponse, DashboardRecentStudentResponse
from app.schemas.dashboard_activity import MentorActivityResponse


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
            select(func.count(StudentUpdate.id)).where(
                StudentUpdate.is_published.is_(True),
                StudentUpdate.is_deleted.is_(False),
            )
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

    @staticmethod
    def _is_today(dt: datetime | None) -> bool:
        if dt is None:
            return False
        now = datetime.now(UTC)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC).date() == now.date()

    async def list_recent_mentor_activity(self, limit: int = 20) -> list[MentorActivityResponse]:
        return await self.list_recent_activity(limit=limit)

    async def list_recent_activity(self, limit: int = 20) -> list[MentorActivityResponse]:
        activities: list[MentorActivityResponse] = []

        # 1. Grouped student attendance & mentor attendance creation from AttendanceCode
        try:
            attendance_code_stmt = (
                select(AttendanceCode)
                .options(
                    selectinload(AttendanceCode.attendances),
                    selectinload(AttendanceCode.mentor),
                )
                .order_by(AttendanceCode.created_at.desc())
                .limit(limit)
            )
            code_res = await self.session.execute(attendance_code_stmt)
            codes = code_res.scalars().all()
            for code in codes:
                mentor_name = code.mentor.full_name if code.mentor else "Mentor"

                # (a) Mentor created attendance event
                if code.created_at:
                    is_today = self._is_today(code.created_at)
                    time_str = code.created_at.strftime("%I:%M %p").lower().lstrip("0")
                    if is_today:
                        create_desc = f"{mentor_name} created attendance at {time_str} today"
                    else:
                        create_desc = f"{mentor_name} created attendance at {time_str} on {code.created_at.strftime('%b %d')}"

                    activities.append(
                        MentorActivityResponse(
                            id=code.id + 2000000,
                            actor_user_id=code.mentor.user_id if code.mentor else None,
                            actor_name=mentor_name,
                            programme=code.programme,
                            track=code.track,
                            action="attendance_code_created",
                            description=create_desc,
                            created_at=code.created_at,
                        )
                    )

                # (b) Student attendance signing group event
                if code.attendances:
                    sorted_attendances = sorted(
                        code.attendances,
                        key=lambda a: a.created_at or datetime.min.replace(tzinfo=UTC),
                    )
                    total_signed = len(sorted_attendances)
                    first_student = sorted_attendances[0].student_name or "A student"
                    latest_att = sorted_attendances[-1]
                    latest_time = latest_att.created_at or code.created_at

                    is_today = self._is_today(latest_time)
                    others = total_signed - 1
                    other_word = "other" if others == 1 else "others"

                    if is_today:
                        if others > 0:
                            desc = f"{first_student} and {others} {other_word} in class signed attendance today"
                        else:
                            desc = f"{first_student} in class signed attendance today"
                    else:
                        date_str = latest_time.strftime("%b %d")
                        if others > 0:
                            desc = f"{first_student} and {others} {other_word} in class signed attendance on {date_str}"
                        else:
                            desc = f"{first_student} in class signed attendance on {date_str}"

                    activities.append(
                        MentorActivityResponse(
                            id=latest_att.id + 1000000,
                            actor_user_id=None,
                            actor_name=first_student,
                            programme=code.programme,
                            track=code.track,
                            action="attendance_signed_group",
                            description=desc,
                            created_at=latest_time,
                        )
                    )
        except Exception:
            pass

        # 2. General audit logs (announcements, course materials, assessments, profiles, etc.)
        try:
            audit_stmt = (
                select(AuditLog, User, Mentor, StudentProfile)
                .outerjoin(User, AuditLog.actor_user_id == User.id)
                .outerjoin(Mentor, Mentor.user_id == User.id)
                .outerjoin(StudentProfile, StudentProfile.user_id == User.id)
                .where(AuditLog.action != "student_attendance_signed")
                .order_by(AuditLog.created_at.desc())
                .limit(limit)
            )
            audit_res = await self.session.execute(audit_stmt)
            rows = audit_res.all()

            for row in rows:
                if len(row) == 4:
                    audit_log, user, mentor, profile = row
                elif len(row) == 3:
                    audit_log, user, mentor = row
                    profile = None
                elif len(row) == 2:
                    audit_log, user = row
                    mentor, profile = None, None
                else:
                    audit_log = row[0]
                    user, mentor, profile = None, None, None

                # Avoid duplicate attendance code creation if already captured
                if audit_log.action == "attendance_code_created":
                    continue

                if mentor and mentor.full_name:
                    actor_name = mentor.full_name
                    prog = mentor.programme
                    trk = mentor.track
                elif profile and profile.full_name:
                    actor_name = profile.full_name
                    prog = profile.programme
                    trk = profile.track
                elif audit_log.after_json and "mentor_name" in audit_log.after_json:
                    actor_name = audit_log.after_json["mentor_name"]
                    prog = audit_log.after_json.get("programme")
                    trk = audit_log.after_json.get("track")
                elif audit_log.after_json and "student_name" in audit_log.after_json:
                    actor_name = audit_log.after_json["student_name"]
                    prog = audit_log.after_json.get("programme")
                    trk = audit_log.after_json.get("track")
                elif user and user.email:
                    actor_name = user.email.split("@")[0].replace(".", " ").title()
                    prog, trk = None, None
                else:
                    actor_name = "User"
                    prog, trk = None, None

                desc = self._build_activity_description(
                    actor_name=actor_name,
                    programme=prog,
                    track=trk,
                    action=audit_log.action,
                    created_at=audit_log.created_at,
                    after_json=audit_log.after_json,
                )

                activities.append(
                    MentorActivityResponse(
                        id=audit_log.id,
                        actor_user_id=user.id if user else None,
                        actor_name=actor_name,
                        programme=prog,
                        track=trk,
                        action=audit_log.action,
                        description=desc,
                        created_at=audit_log.created_at,
                    )
                )
        except Exception:
            pass

        activities.sort(
            key=lambda a: a.created_at or datetime.min.replace(tzinfo=UTC),
            reverse=True,
        )
        return activities[:limit]

    @classmethod
    def _build_activity_description(
        cls,
        actor_name: str | None = None,
        programme: str | None = None,
        track: str | None = None,
        action: str = "",
        created_at: datetime | None = None,
        after_json: dict | None = None,
        mentor_name: str | None = None,
    ) -> str:
        name = actor_name or mentor_name or "User"
        after = after_json or {}
        title = after.get("title")
        prog_track = f" for {programme} ({track})" if programme or track else ""
        is_today = cls._is_today(created_at) if created_at else True
        time_str = created_at.strftime("%I:%M %p").lower().lstrip("0") if created_at else ""

        if action == "attendance_code_created":
            if is_today and time_str:
                return f"{name} created attendance at {time_str} today"
            return f"{name} created attendance at {time_str}" if time_str else f"{name} created attendance"

        elif action == "student_update_created":
            if title:
                return f"{name} posted an announcement: \"{title}\""
            return f"{name} the mentor{prog_track} just posted an announcement"

        elif action == "student_update_updated":
            if title:
                return f"{name} updated announcement: \"{title}\""
            return f"{name} updated an announcement"

        elif action == "student_update_deleted":
            return f"{name} deleted an announcement"

        elif action == "course_material_created":
            if title:
                return f"{name} uploaded course material: \"{title}\""
            return f"{name} the mentor{prog_track} just uploaded a course material"

        elif action == "course_material_updated":
            if title:
                return f"{name} updated course material: \"{title}\""
            return f"{name} the mentor{prog_track} just updated a course material"

        elif action == "course_material_deleted":
            return f"{name} deleted a course material"

        elif action == "mentor_assessment_created":
            if title:
                return f"{name} created assessment: \"{title}\""
            return f"{name} the mentor{prog_track} just created an assessment"

        elif action == "mentor_assessment_updated":
            if title:
                return f"{name} updated assessment: \"{title}\""
            return f"{name} updated an assessment"

        elif action == "mentor_assessment_released":
            if title:
                return f"{name} released assessment: \"{title}\""
            return f"{name} the mentor{prog_track} just released an assessment"

        elif action == "assessment_result_graded":
            return f"{name} graded assessment submissions"

        elif action == "assessment_submitted":
            if title:
                return f"{name} submitted assessment: \"{title}\""
            return f"{name} submitted an assessment"

        elif action == "account_activated":
            return f"{name} activated their portal account"

        elif action == "email_verified":
            return f"{name} verified their email address"

        elif action == "profile_updated":
            return f"{name} updated their profile"

        elif action == "student_discord_invite_generated":
            return f"{name} generated a Discord invite"

        elif action in ("student_invited_by_admin", "portal_user_invited"):
            invited_email = after.get("email")
            if invited_email:
                return f"{name} invited {invited_email} to the portal"
            return f"{name} invited a new user"

        elif action == "student_created":
            return f"{name} registered a new student"

        elif action == "student_updated":
            return f"{name} updated a student profile"

        elif action == "student_archived":
            return f"{name} archived a student account"

        elif action == "student_evicted":
            return f"{name} evicted a student"

        elif action == "student_participation_updated":
            part = after.get("participation")
            if part:
                return f"{name} updated student participation to {part}"
            return f"{name} updated student participation"

        elif action == "mentor_created":
            m_name = after.get("full_name")
            if m_name:
                return f"{name} added mentor {m_name}"
            return f"{name} added a new mentor"

        elif action == "mentor_updated":
            return f"{name} updated mentor details"

        elif action == "mentor_deleted":
            return f"{name} removed a mentor"

        elif action == "mentor_course_assigned":
            return f"{name} assigned a mentor to a course"

        elif action == "mentor_course_removed":
            return f"{name} removed a mentor from a course"

        elif action == "sync_triggered_by_admin":
            return f"{name} triggered a system sync"

        elif action == "sync_triggered_by_system":
            return "Automated system sync completed"

        else:
            friendly_action = action.replace("_", " ")
            return f"{name} the mentor{prog_track} performed: {friendly_action}" if prog_track else f"{name} performed: {friendly_action}"
