from typing import Optional, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from modules.posts.dto.create_post_dto import CreatePostDTO
from modules.posts.dto.post_response_dto import PostResponseDTO
from modules.posts.dto.update_post import UpdatePostDTO
from modules.posts.use_cases.create_post import CreatePost
from modules.posts.use_cases.delete_post import DeletePost
from modules.posts.use_cases.get_by_id_post import GetPostById
from modules.posts.use_cases.get_tags_by_id import get_tags_by_id
from modules.posts.use_cases.list_post import ListPosts
from modules.posts.use_cases.update_post import UpdatePost


async def create_post_service(
        db: AsyncSession,
        post_data: CreatePostDTO,
        user_id: str
) -> Optional[PostResponseDTO]:
    tags = await get_tags_by_id(db, post_data.tag_ids)

    post = await CreatePost.create_post(db, post_data, user_id, tags)

    return PostResponseDTO(
        id=post.id,
        title=post.title,
        author_id=post.author_id,
        content=post.content,
        created_at=post.created_at,
        updated_at=post.updated_at
    )

async def update_post_service(
    db: AsyncSession,
    post_id: UUID,
    user_id: UUID,
    update_data: UpdatePostDTO
) -> Optional[PostResponseDTO]:

    post = await GetPostById.get_post_by_id(db, post_id)

    tags = await get_tags_by_id(db, update_data.tag_ids)

    if not post:
        return None

    if str(user_id) != str(post.author_id):
        raise ValueError(f"User {user_id} is not the author of Post {post_id}")

    post_updated = await UpdatePost.update_post(db, post, tags, update_data)

    if not post_updated:
        raise ValueError("Post not found")

    return PostResponseDTO(
        id=post_updated.id,
        title=post_updated.title,
        author_id=post_updated.author_id,
        content=post_updated.content,
        tags=post_updated.tags,
        created_at=post_updated.created_at,
        updated_at=post_updated.updated_at
    )

async def delete_post_service(
    db: AsyncSession,
    post_id: UUID,
    user_id: UUID
) -> bool:

    post = await GetPostById.get_post_by_id(db, post_id)

    if not post:
        return False

    if str(user_id) != str(post.author_id):
        raise ValueError(f"User {user_id} is not the author of Post {post_id}")

    is_delete = await DeletePost.delete_post(db, post)

    if not is_delete:
        raise ValueError("Post not found")

    return is_delete

async def get_post_by_id_service(
    db: AsyncSession,
    post_id: UUID,
) -> Optional[PostResponseDTO]:

    post = await GetPostById.get_post_by_id(db, post_id)

    return PostResponseDTO(
        id=post.id,
        title=post.title,
        author_id=post.author_id,
        content=post.content,
        tags=post.tags,
        comments=post.comments,
        created_at=post.created_at,
        updated_at=post.updated_at
    )

async def list_post_service(
    db: AsyncSession,
    page: int ,
    page_size: int
) -> Optional[List[PostResponseDTO]]:

    posts = await ListPosts.list_posts(db, page, page_size)

    return [
        PostResponseDTO(
            id=post.id,
            title=post.title,
            author_id=post.author_id,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
            tags=post.tags,
            comments=post.comments
        )
        for post in posts
    ]



