from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.comment.dto.response_comment import ResponseCommentDTO
from modules.posts.dto.post_response_dto import PostResponseDTO
from modules.posts.model.model import PostModel


class ListPosts:
    @staticmethod
    async def list_posts(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10
    ) -> List[PostResponseDTO]:
        try:
            skip = (page - 1) * page_size

            stmt = (PostModel.
                    get_active_stmt()
                    .options(
                        selectinload(PostModel.tags),
                        selectinload(PostModel.comments)
                    )
                    .offset(skip)
                    .limit(page_size)
                    .order_by(PostModel.created_at.desc()))

            result = await db.execute(stmt)
            posts = result.scalars().all()

            return [
                PostResponseDTO(
                    id=post.id,
                    title=post.title,
                    content=post.content,
                    author_id=post.author_id,
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                    tags=post.tags,
                    comments=[
                        ResponseCommentDTO(
                            id=comment.id,
                            content=comment.content,
                            post_id=comment.post_id,
                            created_at=comment.created_at,
                            author_id=comment.author_id
                        ) for comment in post.comments
                    ]
                )
                for post in posts
            ]

        except Exception as e:
            raise ValueError(f"Error listing posts: {str(e)}")
