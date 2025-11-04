from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from modules.comment.dto.request_comment_dto import RequestCommentDTO
from modules.comment.model.model import CommentModel


class CreateComment:
    @staticmethod
    async def create_comment(
        db: AsyncSession,
        comment_data: RequestCommentDTO,
        user_id: str
) -> Optional[CommentModel]:
        try:
            new_comment = CommentModel(
                id=uuid4(),
                content=comment_data.content,
                post_id=comment_data.post_id,
                author_id=user_id
            )

            db.add(new_comment)
            await db.commit()
            await db.refresh(new_comment)

            return new_comment
        except IntegrityError:
            await db.rollback()
            raise ValueError("Repeated values")
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error: {str(e)}")