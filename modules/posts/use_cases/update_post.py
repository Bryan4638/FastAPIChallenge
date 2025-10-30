from typing import Optional
from uuid import UUID

from sqlalchemy import update, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from modules.posts.dto.update_post import UpdatePostDTO
from modules.posts.model.model import PostModel


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
            query = (select(PostModel)
                     .where(
                PostModel.id == post_id,
                PostModel.author_id == user_id,
                PostModel.is_deleted == False)
            )
            result = await db.execute(query)
            post = result.scalar_one_or_none()

            if not post:
                return None

            update_values = {}
            if update_data.title is not None:
                update_values['title'] = update_data.title
            if update_data.content is not None:
                update_values['content'] = update_data.content

            if not update_values:
                return None

            await db.execute(
                update(PostModel)
                .where(PostModel.id == post_id)
                .values(**update_values)
            )

            await db.commit()
            await db.refresh(post)

            return post

        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error while updating post: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error updating post: {str(e)}")