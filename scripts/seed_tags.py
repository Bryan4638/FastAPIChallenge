import asyncio
from uuid import uuid4

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.database import Base
from modules.posts.model.model import TagModel, PostModel

from modules.comment.model.model import CommentModel

SAMPLE_TAGS = [
    {"name": "programming"},
    {"name": "python"},
    {"name": "fastapi"},
    {"name": "sqlalchemy"},
    {"name": "docker"},
    {"name": "testing"},
    {"name": "web"},
    {"name": "development"},
    {"name": "database"},
    {"name": "api"}
]

async def seed_tags():
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM tags"))
        count = result.scalar_one()
        
        if count > 0:
            print(f"Database already contains {count} tags. No new tags were added.")
            return
            
        for tag_data in SAMPLE_TAGS:
            tag = TagModel(**tag_data)
            session.add(tag)
        
        await session.commit()
        print(f"Successfully added {len(SAMPLE_TAGS)} tags to the database.")

if __name__ == "__main__":
    print("Starting to seed tags...")
    asyncio.run(seed_tags())
    print("Finished seeding tags.")
