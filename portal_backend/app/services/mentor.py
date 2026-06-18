from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.portal import (
    AuditLog,
    CourseMaterial,
    Mentor,
    MentorCourseMap,
    ParticipationMode,
    StudentProfile,
    StudentUpdate,
    UpdateTargetType,
    User,
    UserRole,
)
from app.schemas.courses import AdminCourseSummaryResponse
from app.schemas.mentor import (
    CreateMentorUpdateRequest,
    MentorStudentResponse,
)
from app.schemas.portal_management import (
    CourseMaterialCreateRequest,
    CourseMaterialResponse,
    CourseMaterialUpdateRequest,
)
from app.schemas.students import StudentParticipationResponse
from app.schemas.updates import CreateStudentUpdateRequest, StudentUpdateResponse
from app.services.portal_management import PortalManagementService
from app.services.updates import UpdatesService

settings = get_settings()
_portal_schema = settings.POSTGRES_SCHEMA


class MentorPortalService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_course_update(
        self, *, actor: User, payload: CreateMentorUpdateRequest
    ) -> StudentUpdateResponse:
        mentor = await self._require_mentor(actor)
        await self._ensure_course_assigned(mentor=mentor, course_id=payload.course_id)
        update_payload = CreateStudentUpdateRequest(
            title=payload.title,
            body=payload.body,
            target_type=UpdateTargetType.COURSE,
            target_ref=str(payload.course_id),
            is_published=payload.is_published,
            send_in_app=payload.send_in_app,
            send_email=payload.send_email,
        )
        return await UpdatesService(self.session).create_update(actor=actor, payload=update_payload)

    async def list_course_updates(
        self, *, actor: User, course_id: int | None = None
    ) -> list[StudentUpdateResponse]:
        mentor = await self._require_mentor(actor)
        course_ids = await self._assigned_course_ids(mentor.id)
        if not course_ids:
            return []
        if course_id is not None:
            await self._ensure_course_assigned(mentor=mentor, course_id=course_id)
            course_ids = [course_id]

        statement = (
            select(StudentUpdate)
            .where(
                StudentUpdate.created_by == actor.id,
                StudentUpdate.target_type == UpdateTargetType.COURSE.value,
                StudentUpdate.target_ref.in_([str(cid) for cid in course_ids]),
            )
            .order_by(StudentUpdate.created_at.desc())
        )
        result = await self.session.execute(statement)
        updates_service = UpdatesService(self.session)
        return [
            updates_service._build_update_response(student_update=item)
            for item in result.scalars().all()
        ]

    async def list_course_summaries(self, *, actor: User) -> list[AdminCourseSummaryResponse]:
        mentor = await self._require_mentor(actor)
        course_ids = await self._assigned_course_ids(mentor.id)
        if not course_ids:
            return []

        statement = text(
            """
            SELECT
                c.id AS course_id,
                c.name AS course_name,
                COUNT(p.id) AS total_students,
                SUM(CASE WHEN UPPER(COALESCE(p.status, '')) = 'ACCEPTED' THEN 1 ELSE 0 END) AS accepted_students,
                SUM(CASE WHEN p.payment_status = TRUE THEN 1 ELSE 0 END) AS paid_students
            FROM cohort_course AS c
            LEFT JOIN cohort_participant AS p ON p.course_id = c.id
            WHERE c.id = ANY(:course_ids)
            GROUP BY c.id, c.name
            ORDER BY c.name ASC
            """
        )
        result = await self.session.execute(statement, {"course_ids": course_ids})
        rows = [dict(row._mapping) for row in result.all()]
        return [AdminCourseSummaryResponse(**row) for row in rows]

    async def list_materials(
        self, *, actor: User, course_id: int | None = None
    ) -> list[CourseMaterial]:
        mentor = await self._require_mentor(actor)
        allowed_ids = await self._assigned_course_ids(mentor.id)
        if not allowed_ids:
            return []
        if course_id is not None:
            await self._ensure_course_assigned(mentor=mentor, course_id=course_id)
            allowed_ids = [course_id]

        statement = (
            select(CourseMaterial)
            .where(CourseMaterial.course_id.in_(allowed_ids))
            .order_by(CourseMaterial.created_at.desc())
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create_material(
        self, *, actor: User, payload: CourseMaterialCreateRequest
    ) -> CourseMaterialResponse:
        mentor = await self._require_mentor(actor)
        await self._ensure_course_assigned(mentor=mentor, course_id=payload.course_id)
        return await PortalManagementService(self.session).create_course_material(
            actor=actor, payload=payload
        )

    async def update_material(
        self, *, actor: User, material_id: int, payload: CourseMaterialUpdateRequest
    ) -> CourseMaterialResponse:
        mentor = await self._require_mentor(actor)
        material = await PortalManagementService(self.session)._get_material(material_id)
        await self._ensure_course_assigned(mentor=mentor, course_id=material.course_id)
        return await PortalManagementService(self.session).update_course_material(
            actor=actor, material_id=material_id, payload=payload
        )

    async def delete_material(self, *, actor: User, material_id: int) -> None:
        mentor = await self._require_mentor(actor)
        material = await PortalManagementService(self.session)._get_material(material_id)
        await self._ensure_course_assigned(mentor=mentor, course_id=material.course_id)
        await PortalManagementService(self.session).delete_course_material(
            actor=actor, material_id=material_id
        )

    async def list_students(
        self, *, actor: User, course_id: int | None = None
    ) -> list[MentorStudentResponse]:
        mentor = await self._require_mentor(actor)
        course_ids = await self._assigned_course_ids(mentor.id)
        if not course_ids:
            return []
        if course_id is not None:
            await self._ensure_course_assigned(mentor=mentor, course_id=course_id)
            course_ids = [course_id]

        statement = text(
            f"""
            SELECT
                p.name AS participant_name,
                LOWER(TRIM(p.email)) AS email,
                c.id AS course_id,
                c.name AS course_name,
                p.cohort AS cohort,
                p.status AS approval_status,
                p.payment_status AS payment_status,
                u.id AS portal_user_id,
                u.account_state AS account_state,
                COALESCE(p.updated_at, p.created_at) AS source_updated_at
            FROM cohort_participant AS p
            INNER JOIN cohort_course AS c ON c.id = p.course_id
            LEFT JOIN {_portal_schema}.users AS u
                ON LOWER(TRIM(u.email)) = LOWER(TRIM(p.email))
                AND u.role = :student_role
            WHERE p.course_id = ANY(:course_ids)
            ORDER BY c.name ASC, p.name ASC, p.email ASC
            """
        )
        result = await self.session.execute(
            statement,
            {"course_ids": course_ids, "student_role": UserRole.STUDENT.value},
        )
        return [MentorStudentResponse(**dict(row._mapping)) for row in result.all()]

    async def set_student_participation(
        self,
        *,
        actor: User,
        portal_user_id: int,
        participation: ParticipationMode | None,
    ) -> StudentParticipationResponse:
        mentor = await self._require_mentor(actor)
        course_ids = await self._assigned_course_ids(mentor.id)
        if not course_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to any courses",
            )

        student = await self.session.execute(
            select(User).where(
                User.id == portal_user_id, User.role == UserRole.STUDENT.value
            )
        )
        student_user = student.scalar_one_or_none()
        if student_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
            )

        enrollment = await self.session.execute(
            text(
                """
                SELECT 1
                FROM cohort_participant AS p
                WHERE LOWER(TRIM(p.email)) = :email
                  AND p.course_id = ANY(:course_ids)
                LIMIT 1
                """
            ),
            {"email": student_user.email.lower().strip(), "course_ids": course_ids},
        )
        if enrollment.first() is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This student is not enrolled in any of your assigned courses",
            )

        profile_result = await self.session.execute(
            select(StudentProfile).where(StudentProfile.user_id == portal_user_id)
        )
        profile = profile_result.scalar_one_or_none()
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )

        before = {"participation": profile.participation}
        profile.participation = participation.value if participation is not None else None
        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="student_participation_updated",
                resource_type="student",
                resource_id=str(portal_user_id),
                before_json=before,
                after_json={"participation": profile.participation},
                created_at=datetime.now(UTC),
            )
        )
        await self.session.commit()
        await self.session.refresh(profile)
        return StudentParticipationResponse(
            user_id=student_user.id,
            email=student_user.email,
            full_name=profile.full_name,
            participation=profile.participation,
        )

    async def _require_mentor(self, actor: User) -> Mentor:
        result = await self.session.execute(
            select(Mentor).where(Mentor.user_id == actor.id, Mentor.is_active.is_(True))
        )
        mentor = result.scalar_one_or_none()
        if mentor is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Active mentor profile required",
            )
        return mentor

    async def _assigned_course_ids(self, mentor_id: int) -> list[int]:
        result = await self.session.execute(
            select(MentorCourseMap.course_id)
            .where(MentorCourseMap.mentor_id == mentor_id)
            .order_by(MentorCourseMap.course_id.asc())
        )
        return list(result.scalars().all())

    async def _ensure_course_assigned(self, *, mentor: Mentor, course_id: int) -> None:
        course_ids = await self._assigned_course_ids(mentor.id)
        if course_id not in course_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to this course",
            )
