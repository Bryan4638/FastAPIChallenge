from typing import Optional
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from modules.comment.model.model import CommentModel
from modules.comment.use_cases.find_by_id import FindCommentById
from modules.posts.dto.update_post import UpdatePostDTO
from modules.posts.model.model import PostModel
from modules.posts.use_cases.get_by_id_post import GetPostById


class UpdateComment:
    @classmethod
    async def update_post(
        cls,
        db: AsyncSession,
        post_id: UUID,
        comment_id: UUID,
        user_id: UUID,
        update_content: str
    ) -> Optional[CommentModel]:

        try:
            comment = await FindCommentById.find_by_id(db, post_id, comment_id)

            if not comment:
                return None

            if not user_id.__eq__(comment.author_id):
                return None

            update_values = {}
            if update_content is not None:
                update_values['content'] = update_content

            if not update_values:
                return None

            await db.execute(
                update(CommentModel)
                .where((CommentModel.id == comment_id) & (CommentModel.author_id == user_id))
                .values(**update_values)
            )

            await db.commit()
            await db.refresh(comment)

            return comment

        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error while updating post: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error updating post: {str(e)}")