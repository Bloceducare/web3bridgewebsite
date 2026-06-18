from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.portal import CourseMaterial, User, UserRole
from app.schemas.student import StudentMentorResponse

settings = get_settings()
_portal_schema = settings.POSTGRES_SCHEMA


class StudentPortalService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_materials(
        self, *, user: User, course_id: int | None = None
    ) -> list[CourseMaterial]:
        self._ensure_student_role(user)
        course_ids = await self._enrolled_course_ids(user)
        if not course_ids:
            return []
        if course_id is not None:
            self._ensure_enrolled(course_id=course_id, course_ids=course_ids)
            course_ids = [course_id]

        statement = (
            select(CourseMaterial)
            .where(CourseMaterial.course_id.in_(course_ids))
            .order_by(CourseMaterial.created_at.desc())
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def list_mentors(
        self, *, user: User, course_id: int | None = None
    ) -> list[StudentMentorResponse]:
        self._ensure_student_role(user)
        course_ids = await self._enrolled_course_ids(user)
        if not course_ids:
            return []
        if course_id is not None:
            self._ensure_enrolled(course_id=course_id, course_ids=course_ids)
            course_ids = [course_id]

        statement = text(
            f"""
            SELECT
                m.id AS id,
                m.full_name AS full_name,
                m.email AS email,
                m.bio AS bio,
                array_agg(DISTINCT mcm.course_id) AS course_ids
            FROM {_portal_schema}.mentors AS m
            INNER JOIN {_portal_schema}.mentor_course_map AS mcm
                ON mcm.mentor_id = m.id
            WHERE m.is_active = TRUE
              AND mcm.course_id = ANY(:course_ids)
            GROUP BY m.id, m.full_name, m.email, m.bio
            ORDER BY m.full_name ASC
            """
        )
        result = await self.session.execute(statement, {"course_ids": course_ids})
        return [StudentMentorResponse(**dict(row._mapping)) for row in result.all()]

    async def _enrolled_course_ids(self, user: User) -> list[int]:
        statement = text(
            """
            SELECT DISTINCT p.course_id
            FROM cohort_participant AS p
            WHERE LOWER(TRIM(p.email)) = :email
              AND p.course_id IS NOT NULL
            """
        )
        result = await self.session.execute(
            statement, {"email": user.email.lower().strip()}
        )
        return [int(row[0]) for row in result.all()]

    @staticmethod
    def _ensure_student_role(user: User) -> None:
        if user.role != UserRole.STUDENT.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student access required",
            )

    @staticmethod
    def _ensure_enrolled(*, course_id: int, course_ids: list[int]) -> None:
        if course_id not in course_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not enrolled in this course",
            )
