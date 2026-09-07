from datetime import datetime
from pydantic import BaseModel

class MentorActivityResponse(BaseModel):
    id: int
    actor_user_id: int
    actor_name: str
    programme: str | None = None
    track: str | None = None
    action: str
    description: str
    created_at: datetime
