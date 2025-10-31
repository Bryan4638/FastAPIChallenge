from uuid import UUID

from pydantic import BaseModel, Field

class RequestCommentDTO(BaseModel):
    content: str = Field(..., min_length=2, max_length=500, description="Unique username")
    post_id: UUID = Field(..., description="Post Id")
