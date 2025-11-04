from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from modules.comment.model.model import CommentModel


class FindCommentById:
    @staticmethod
    async def find_by_id(db: AsyncSession, comment_id: UUID) -> Optional[CommentModel]:
        try:
            stmt = (CommentModel.get_active_stmt().where(((CommentModel.id == comment_id) & (CommentModel.is_deleted == False))))

            result = await db.execute(stmt)
            comment = result.scalars().first()

            if not comment:
                return None

            return comment

        except SQLAlchemyError as e:
            raise ValueError(f"Database error while fetching comment: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error fetching comment: {str(e)}")
