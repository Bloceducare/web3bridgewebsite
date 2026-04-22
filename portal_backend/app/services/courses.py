from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import User
from app.schemas.courses import AdminCourseSummaryResponse, StudentCourseResponse


class CoursesService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_my_courses(self, *, user: User) -> list[StudentCourseResponse]:
        statement = text(
            """
            SELECT
                c.id AS course_id,
                c.name AS course_name,
                p.cohort AS cohort,
                p.status AS approval_status,
                p.payment_status AS payment_status,
                COALESCE(p.updated_at, p.created_at) AS source_updated_at
            FROM cohort_participant AS p
            LEFT JOIN cohort_course AS c ON c.id = p.course_id
            WHERE LOWER(TRIM(p.email)) = :email
            ORDER BY COALESCE(p.updated_at, p.created_at) DESC, p.id DESC
            """
        )
        result = await self.session.execute(statement, {"email": user.email.lower().strip()})
        rows = [dict(row._mapping) for row in result.all()]
        return [StudentCourseResponse(**row) for row in rows]

    async def list_admin_course_summaries(self) -> list[AdminCourseSummaryResponse]:
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
            GROUP BY c.id, c.name
            ORDER BY c.name ASC
            """
        )
        result = await self.session.execute(statement)
        rows = [dict(row._mapping) for row in result.all()]
        return [AdminCourseSummaryResponse(**row) for row in rows]
