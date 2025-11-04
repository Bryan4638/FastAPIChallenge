from typing import Optional
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from modules.comment.dto.request_comment_dto import RequestCommentDTO
from modules.comment.model.model import CommentModel


class UpdateComment:
    @classmethod
    async def update_comment(
        cls,
        db: AsyncSession,
        comment_id: UUID,
        user_id: UUID,
        comment: CommentModel,
        update_data: RequestCommentDTO
    ) -> Optional[CommentModel]:
        try:

            update_values = {}
            if update_data.content is not None:
                update_values['content'] = update_data.content

            if update_data.post_id is not None:
                update_values['post_id'] = update_data.post_id

            if not update_values:
                raise ValueError("No fields to update")

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
            raise ValueError(f"Database error while updating comment: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error updating comment: {str(e)}")