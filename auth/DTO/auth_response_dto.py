from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class TokenData(BaseModel):
    access_token: str = Field(..., description="JWT access token")

class UserResponse(BaseModel):
    id: UUID = Field(..., description="User's unique identifier")
    username: str = Field(..., description="User's username")
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    created_at: datetime = Field(..., description="When the user was created")

class AuthResponseDTO(BaseModel):
    user: UserResponse = Field(..., description="User information")
    access_token: str = Field(..., description="JWT access token")

class RegisterResponseDTO(BaseModel):
    message: str = Field(..., description="Success message")
    response: AuthResponseDTO = Field(..., description="User information and token")