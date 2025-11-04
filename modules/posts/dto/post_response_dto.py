from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

from modules.comment.dto.response_comment import ResponseCommentDTO


class TagBase(BaseModel):
    id:UUID
    name: str

    class Config:
        from_attributes = True


class PostResponseDTO(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the post")
    title: str = Field(..., max_length=200, description="Title of the post")
    author_id: UUID = Field(..., description="Unique identifier of the author")
    content: str = Field(..., description="Content of the post")
    created_at: datetime = Field(..., description="When the post was created")
    updated_at: datetime = Field(..., description="When the post was last updated")
    tags: List[TagBase] = Field(default_factory=list)
    comments: List[ResponseCommentDTO] = Field(default_factory=list)

