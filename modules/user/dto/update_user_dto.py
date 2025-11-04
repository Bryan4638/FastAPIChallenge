import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UpdateUserDTO(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50, description="User's first name", examples=["John"])
    last_name: Optional[str] = Field(None, max_length=50, description="User's last name", examples=["Doe"])
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="New password (min 8 characters)", examples=["newSecurePassword123"])

    @field_validator('password')
    def password_strength(cls, v):
        if v is not None:
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters long")
            if not re.search("[a-z]", v):
                raise ValueError("Password must contain at least one lowercase letter")
            if not re.search("[A-Z]", v):
                raise ValueError("Password must contain at least one uppercase letter")
            if not re.search("[0-9]", v):
                raise ValueError("Password must contain at least one number")
        return v

    class Config:
        from_attributes = True
