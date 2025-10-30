from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.database import Base
from core.mixin_soft_delete import SoftDeleteMixin
from core.mixin_timestamp import TimestampMixin


class UserModel(SoftDeleteMixin, TimestampMixin, Base):
    __tablename__ = "user"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(String(100), nullable=False, index=True)
    password= Column(String(500), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)


    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name})"

