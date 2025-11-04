from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.mixin_soft_delete import SoftDeleteMixin
from core.mixin_timestamp import TimestampMixin

post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id',
        PG_UUID(as_uuid=True),
        ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', PG_UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)
)


class PostModel(SoftDeleteMixin, TimestampMixin, Base):
    __tablename__ = "posts"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(PG_UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)

    tags = relationship("TagModel", secondary=post_tags, back_populates="posts")
    comments = relationship("CommentModel", backref="post", lazy="selectin")

    def __repr__(self):
        return f"<Post {self.title}>"


class TagModel(Base):
    __tablename__ = "tags"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(50), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    posts = relationship("PostModel", secondary=post_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name}>"