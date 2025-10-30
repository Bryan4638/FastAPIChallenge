from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from modules.posts.model.model import PostModel


class GetPostById:
    @staticmethod
    async def get_post_by_id(
        db: AsyncSession,
        post_id: UUID,
        user_id: UUID
    ) -> Optional[PostModel]:
        try:
            result = await db.execute(
                select(PostModel)
                .where(
                    (PostModel.id == post_id) &
                    (PostModel.author_id == user_id) &
                    (PostModel.is_deleted == False)
                )
            )
            
            post = result.scalars().first()
            
            if not post:
                return None
                
            return post
            
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while fetching post: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error fetching post: {str(e)}")
