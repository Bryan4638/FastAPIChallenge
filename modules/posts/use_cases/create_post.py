from typing import Optional, List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from modules.posts.dto.create_post_dto import CreatePostDTO
from modules.posts.model.model import PostModel, TagModel


class CreatePost:
    @staticmethod
    async def create_post(db: AsyncSession,
        post_data: CreatePostDTO,
        user_id: str,
        tags: List[TagModel]
) -> Optional[PostModel]:
        try:

            new_post = PostModel(
                id=uuid4(),
                title=post_data.title,
                content=post_data.content,
                author_id=user_id,
                tags=tags,
            )

            db.add(new_post)
            await db.commit()
            await db.refresh(new_post)

            return new_post
        except IntegrityError:
            await db.rollback()
            raise ValueError("Repeated values")
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error: {str(e)}")