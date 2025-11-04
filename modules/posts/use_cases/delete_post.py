from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from modules.posts.model.model import PostModel


class DeletePost:
    @staticmethod
    async def delete_post(
        db: AsyncSession,
        post: PostModel
    ) -> bool:
        try:

            post.soft_delete()
            await db.commit()

            return True
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Error de base de datos al eliminar el post: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error al eliminar el post: {str(e)}")
