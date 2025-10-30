from pydantic import BaseModel, Field, field_validator


class CreatePostDTO(BaseModel):
    title: str = Field(..., min_length=5, max_length=200, description="Title of the post (5-200 characters)")
    content: str = Field(..., min_length=5, description="Main content of the post (minimum 5 characters)")

    @field_validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or just whitespace")
        return v.strip()

    @field_validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty or just whitespace")
        return v.strip()
