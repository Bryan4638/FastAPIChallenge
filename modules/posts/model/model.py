from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from core.database import Base


class PostModel(Base):
    __tablename__ = "post"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)

    author_id = Column(PG_UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


    def __repr__(self):
        return f"<Post {self.title} ({self.content})>"

