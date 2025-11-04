from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class UserResponseDTO(BaseModel):

    id: UUID = Field(..., description="Unique identifier of the user")
    username: str = Field(..., description="User's username")
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    created_at: datetime = Field(..., description="When the user was created")
    updated_at: datetime = Field(..., description="When the user was last updated")

    class Config:
        from_attributes = True