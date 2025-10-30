from uuid import uuid4
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.database import Base
from core.mixin_soft_delete import SoftDeleteMixin
from core.mixin_timestamp import TimestampMixin


class PostModel(SoftDeleteMixin, TimestampMixin,Base):
    __tablename__ = "post"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)

    author_id = Column(PG_UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Post {self.title} ({self.content})>"

