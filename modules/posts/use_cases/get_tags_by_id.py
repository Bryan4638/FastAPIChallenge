from uuid import UUID

from sqlalchemy import select
from ..model.model import TagModel
from sqlalchemy.ext.asyncio import AsyncSession


async def get_tags_by_id(db: AsyncSession, tag_ids: list[UUID]):

    if not tag_ids:
        return []

    query = select(TagModel).where(TagModel.id.in_(tag_ids))
    result = await db.execute(query)
    return result.scalars().all()