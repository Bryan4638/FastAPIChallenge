from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from modules.posts.model.model import PostModel


class GetPostById:
    @staticmethod
    async def get_post_by_id(
        db: AsyncSession,
        post_id: UUID,
    ) -> Optional[PostModel]:
        try:
            stmt = (PostModel.
                    get_active_stmt()
                    .options(
                        selectinload(PostModel.tags),
                        selectinload(PostModel.comments)
                    )
                    .where((PostModel.id == post_id)))

            result = await db.execute(stmt)
            post = result.scalars().first()

            if not post:
                raise ValueError("Post not found")
                
            return post
            
        except SQLAlchemyError as e:
            raise ValueError(f"Database error while fetching post: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error fetching post: {str(e)}")
