from typing import Optional

from pydantic import BaseModel, Field

class UpdatePostDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200, description="Title of the post (5-200 characters)")
    content: Optional[str] = Field(None, min_length=5, description="Main content of the post (minimum 5 characters)")