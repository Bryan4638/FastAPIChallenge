from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from modules.comment.model.model import CommentModel
from modules.posts.model.model import PostModel


class FindCommentById:
    @staticmethod
    async def find_by_id(db: AsyncSession, post_id: UUID, comment_id: UUID) -> Optional[PostModel]:
        try:
            stmt = (CommentModel.get_active_stmt().where((CommentModel.id == comment_id) & (CommentModel.post_id == post_id)))

            result = await db.execute(stmt)
            comment = result.scalars().first()

            if not comment:
                return None

            return comment

        except SQLAlchemyError as e:
            raise ValueError(f"Database error while fetching post: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error fetching post: {str(e)}")
