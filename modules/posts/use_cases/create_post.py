from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from modules.posts.dto.create_post_dto import CreatePostDTO
from modules.posts.model.model import PostModel
from modules.posts.use_cases.get_tags_by_id import get_tags_by_id


class CreatePost:
    @staticmethod
    async def create_post(db: AsyncSession,
        post_data: CreatePostDTO,
        user_id: str
) -> Optional[PostModel]:
        try:

            tags = await get_tags_by_id(db, post_data.tag_ids)

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