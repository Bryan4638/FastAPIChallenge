from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from modules.comment.use_cases.find_by_id import FindCommentById


class DeleteComment:
    @staticmethod
    async def delete_comment(
            db: AsyncSession,
            user_id: UUID,
            comment_id: UUID
    ) -> bool:
        try:
            comment = await FindCommentById.find_by_id(db, comment_id)

            if not comment:
                return False

            if user_id != comment.author_id:
                raise ValueError(f"User {user_id} is not the author of comment {comment_id}")

            comment.soft_delete()
            await db.commit()

            return True

        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Error de base de datos al eliminar el comment: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error al eliminar el comment: {str(e)}")
