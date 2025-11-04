from uuid import UUID

from pydantic import BaseModel


class DeleteResponseDTO(BaseModel):
    message: str = "Deleted successfully"
    id: UUID

    class Config:
        from_attributes = True