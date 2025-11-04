from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class TagResponseDTO(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the tag")
    name: str = Field(..., description="Name of the tag")
    created_at: datetime = Field(..., description="When the tag was created")

    class Config:
        from_attributes = True