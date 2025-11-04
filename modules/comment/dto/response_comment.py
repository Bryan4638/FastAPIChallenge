from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class ResponseCommentDTO(BaseModel):
    id: UUID
    content: str
    post_id: UUID
    author_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True