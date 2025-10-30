from pydantic import BaseModel, Field, field_validator

class LoginDTO(BaseModel):
    username: str = Field(..., description="User name")
    password: str = Field(..., min_length=8, max_length=100, description="User's password")
    
    @field_validator('username','password')
    @classmethod
    def validate_password(cls, v):
        if not v.strip():
            raise ValueError("Password cannot be empty or just whitespace")
        return v.strip()