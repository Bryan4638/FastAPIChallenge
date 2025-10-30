from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from core.database import Base


class UserModel(Base):
    __tablename__ = "user"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(String(100), nullable=False, index=True)
    password= Column(String(500), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name})"

