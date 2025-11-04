from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from modules.comment.model.model import CommentModel


class DeleteComment:
    @staticmethod
    async def delete_comment(
            db: AsyncSession,
            comment: CommentModel
    ) -> bool:
        try:

            comment.soft_delete()
            await db.commit()

            return True

        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Error de base de datos al eliminar el comment: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error al eliminar el comment: {str(e)}")
