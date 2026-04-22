from datetime import datetime

from pydantic import BaseModel


class StudentCourseResponse(BaseModel):
    course_id: int | None = None
    course_name: str
    cohort: str | None = None
    approval_status: str | None = None
    payment_status: bool | None = None
    source_updated_at: datetime | None = None


class AdminCourseSummaryResponse(BaseModel):
    course_id: int
    course_name: str
    total_students: int
    accepted_students: int
    paid_students: int
