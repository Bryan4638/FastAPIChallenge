from sqlalchemy import Column, Boolean, DateTime
from datetime import datetime
from sqlalchemy import select

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None

    @classmethod
    def get_active_stmt(cls):
        return select(cls).where(cls.is_deleted == False)

    @classmethod
    def get_deleted_stmt(cls):
        return select(cls).where(cls.is_deleted == True)

    @classmethod
    def get_all_stmt(cls):
        return select(cls)
