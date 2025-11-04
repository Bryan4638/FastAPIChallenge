from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import select

from modules.posts.model.model import PostModel
from modules.user.use_cases.find_user_by_id import FindUserById


class DeleteUser:
    @staticmethod
    async def delete_user(
        db: AsyncSession,
        user_id: UUID
    ) -> bool:
        try:
            user = await FindUserById.get_by_id(db, user_id)
            if not user or user.is_deleted:
                return False

            user.soft_delete()

            stmt = (
                select(PostModel)
                .where(
                    PostModel.author_id == user_id,
                    PostModel.is_deleted == False
                )
                .execution_options(synchronize_session="fetch")
            )
            
            result = await db.execute(stmt)
            posts = result.scalars().all()
            
            for post in posts:
                post.soft_delete()
            
            await db.commit()
            return True
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error while deleting user: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error deleting user: {str(e)}")
