from uuid import UUID
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from modules.posts.model.model import PostModel
from modules.posts.use_cases.get_by_id_post import GetPostById


class DeletePost:
    @staticmethod
    async def delete_post(
        db: AsyncSession,
        post_id: UUID,
        user_id: UUID
    ) -> bool:
        try:
            post = await GetPostById.get_post_by_id(db, post_id, user_id)

            if not post:
                return False

            await db.execute(
                update(PostModel)
                .where(PostModel.id == post_id)
                .values(is_deleted=True)
            )
            await db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Error de base de datos al eliminar el post: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error al eliminar el post: {str(e)}")
