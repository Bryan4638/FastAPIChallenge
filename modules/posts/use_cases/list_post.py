from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.posts.model.model import PostModel


class ListPosts:
    @staticmethod
    async def list_posts(
        db: AsyncSession,
        user_id: UUID,
        page: int = 0,
        page_size: int = 10
    ) -> List[PostModel]:
        try:

            skip = (page - 1) * page_size
            take = page_size

            result = await db.execute(
                select(PostModel)
                .where(
                    (PostModel.author_id == user_id) &
                    (PostModel.is_deleted == False)  # noqa: E712
                )
                .order_by(PostModel.created_at.desc())
                .offset(skip)
                .limit(take)
            )
            
            posts = result.scalars().all()
            
            return [
                post
                for post in posts
            ]

        except Exception as e:
            raise ValueError(f"Error listing posts: {str(e)}")
