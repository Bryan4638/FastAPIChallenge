from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

class TagBase(BaseModel):
    id:UUID
    name: str

    class Config:
        from_attributes = True

class PostResponseDTO(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the post")
    title: str = Field(..., max_length=200, description="Title of the post")
    content: str = Field(..., description="Content of the post")
    created_at: datetime = Field(..., description="When the post was created")
    updated_at: datetime = Field(..., description="When the post was last updated")
    tags: List[TagBase] = []

