from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from modules.posts.model.model import TagModel

class ListTags:
    @staticmethod
    async def list_tags(db: AsyncSession) -> List[TagModel]:
        try:
            result = await db.execute(select(TagModel).order_by(TagModel.name))
            return list(result.scalars().all())
        except Exception as e:
            raise ValueError(f"Error retrieving tags: {str(e)}")