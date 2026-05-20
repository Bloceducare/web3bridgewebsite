from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import User
from app.schemas.courses import (
    AdminCourseSummaryResponse,
    StudentCourseResponse,
    StudentGuarantorFormResponse,
)


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

    async def get_my_published_guarantor_form(
        self, *, user: User
    ) -> StudentGuarantorFormResponse:
        """
        Return the latest active guarantor form for the student's current cohort.

        Fallback order:
        1) active form matching student's latest participant cohort
        2) active generic form with NULL cohort
        """
        cohort_statement = text(
            """
            SELECT p.cohort
            FROM cohort_participant AS p
            WHERE LOWER(TRIM(p.email)) = :email
            ORDER BY COALESCE(p.updated_at, p.created_at) DESC, p.id DESC
            LIMIT 1
            """
        )
        cohort_result = await self.session.execute(
            cohort_statement, {"email": user.email.lower().strip()}
        )
        cohort = cohort_result.scalar_one_or_none()

        form_statement = text(
            """
            SELECT
                g.id,
                g.title,
                g.form_url,
                g.cohort,
                g.is_active
            FROM guarantor_forms AS g
            WHERE
                g.is_active = TRUE
                AND (
                    (:cohort IS NOT NULL AND g.cohort = :cohort)
                    OR g.cohort IS NULL
                )
            ORDER BY
                CASE WHEN :cohort IS NOT NULL AND g.cohort = :cohort THEN 0 ELSE 1 END,
                g.created_at DESC
            LIMIT 1
            """
        )
        form_result = await self.session.execute(form_statement, {"cohort": cohort})
        row = form_result.mappings().first()
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No published guarantor form is available yet",
            )
        return StudentGuarantorFormResponse(**dict(row))
