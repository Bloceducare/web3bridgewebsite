from pydantic import BaseModel


class StudentMentorResponse(BaseModel):
    id: int
    full_name: str
    email: str
    bio: str | None = None
    course_ids: list[int] = []
