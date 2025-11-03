from typing import Optional
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from modules.posts.dto.update_post import UpdatePostDTO
from modules.posts.model.model import PostModel
from modules.posts.use_cases.get_by_id_post import GetPostById
from modules.posts.use_cases.get_tags_by_id import get_tags_by_id


class UpdatePost:
    @classmethod
    async def update_post(
        cls,
        db: AsyncSession,
        post_id: UUID,
        user_id: UUID,
        update_data: UpdatePostDTO
    ) -> Optional[PostModel]:

        try:
            post = await GetPostById.get_post_by_id(db, post_id, user_id)

            tags = await get_tags_by_id(db, update_data.tag_ids)

            if not post:
                return None

            if not user_id.__eq__(post.author_id):
                return None

            if update_data.title is not None:
                post.title = update_data.title
            if update_data.content is not None:
                post.content = update_data.content
            if update_data.tag_ids is not None:
                post.tags = tags

            if not any([update_data.title, update_data.content, update_data.tag_ids is not None]):
                return None


            db.add(post)
            await db.commit()
            await db.refresh(post)

            return post

        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error while updating post: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error updating post: {str(e)}")