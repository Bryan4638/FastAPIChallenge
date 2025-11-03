from typing import Optional, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from modules.posts.dto.create_post_dto import CreatePostDTO
from modules.posts.dto.post_response_dto import PostResponseDTO
from modules.posts.dto.update_post import UpdatePostDTO
from modules.posts.use_cases.create_post import CreatePost
from modules.posts.use_cases.delete_post import DeletePost
from modules.posts.use_cases.get_by_id_post import GetPostById
from modules.posts.use_cases.list_post import ListPosts
from modules.posts.use_cases.update_post import UpdatePost


async def create_post_service(
        db: AsyncSession,
        post_data: CreatePostDTO,
        user_id: str
) -> Optional[PostResponseDTO]:

    post = await CreatePost.create_post(db, post_data, user_id)

    return PostResponseDTO(
        id=post.id,
        title=post.title,
        content=post.content,
        tags=post.tags,
        created_at=post.created_at,
        updated_at=post.updated_at
    )

async def update_post_service(
    db: AsyncSession,
    post_id: UUID,
    user_id: UUID,
    update_data: UpdatePostDTO
) -> Optional[PostResponseDTO]:

    post = await UpdatePost.update_post(db, post_id, user_id, update_data)

    if not post:
        raise ValueError("Post not found")

    return PostResponseDTO(
        id=post.id,
        title=post.title,
        content=post.content,
        tags=post.tags,
        created_at=post.created_at,
        updated_at=post.updated_at
    )

async def delete_post_service(
    db: AsyncSession,
    post_id: UUID,
    user_id: UUID
) -> bool:

    is_delete = await DeletePost.delete_post(db, post_id, user_id)

    if not is_delete:
        raise ValueError("Post not found")

    return is_delete

async def get_post_by_id_service(
    db: AsyncSession,
    post_id: UUID,
    user_id: UUID
) -> Optional[PostResponseDTO]:

    post = await GetPostById.get_post_by_id(db, post_id, user_id)

    return PostResponseDTO(
        id=post.id,
        title=post.title,
        content=post.content,
        tags=post.tags,
        created_at=post.created_at,
        updated_at=post.updated_at
    )

async def list_post_service(
    db: AsyncSession,
    user_id: UUID,
    page: int ,
    page_size: int
) -> Optional[List[PostResponseDTO]]:

    posts = await ListPosts.list_posts(db, user_id, page, page_size)

    return [
        PostResponseDTO(
            id=post.id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            tags=post.tags,
            updated_at=post.updated_at
        )
        for post in posts
    ]



