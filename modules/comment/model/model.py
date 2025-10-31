from uuid import uuid4
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.database import Base
from core.mixin_soft_delete import SoftDeleteMixin
from core.mixin_timestamp import TimestampMixin


class CommentModel(SoftDeleteMixin, TimestampMixin, Base):
    __tablename__ = "comment"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    content = Column(Text, nullable=False)

    author_id = Column(PG_UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    post_id = Column(PG_UUID(as_uuid=True), ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"<Comment ({self.content})>"

