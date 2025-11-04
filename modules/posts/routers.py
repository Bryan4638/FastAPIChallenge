from typing import Annotated, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from core.config import settings
from core.database import get_session
from core.security import decode_token
from modules.posts.dto.create_post_dto import CreatePostDTO
from modules.posts.dto.post_response_dto import PostResponseDTO
from modules.posts.dto.update_post import UpdatePostDTO
from modules.posts.service.service import (
    create_post_service,
    update_post_service,
    delete_post_service,
    list_post_service,
    get_post_by_id_service
)

# Router
router = APIRouter(
    prefix=f"{settings.API_V1_STR}/post",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
    status_code=status.HTTP_201_CREATED,
    summary="List post",
    description="List a post for the authenticated user"
)
async def get_posts(
        user: Annotated[dict, Depends(decode_token)],
        page: int = 1,
        page_size: int = 10,
        db: AsyncSession = Depends(get_session)
):
    try:

        result = await list_post_service(db, page, page_size)
        [print(post.tags) for post in result]
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{post_id}",
    response_model=Optional[PostResponseDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Get post",
    description="Get a post for the authenticated user"
)
async def get_post_by_id(
        post_id: UUID,
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        return await get_post_by_id_service(db, post_id, user.get("user_id"))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/",
    response_model=PostResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create post",
    description="Create a post for the authenticated user"
)
async def create_post(
        post_data: CreatePostDTO,
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        post = await create_post_service(db, post_data, user.get("user_id"))
        return post
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{post_id}",
    response_model=Optional[PostResponseDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Update post",
    description="Update a post for the authenticated user"
)
async def update_post(
        post_id: UUID,
        update_data: UpdatePostDTO,
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        post = await update_post_service(db, post_id, user.get("user_id"), update_data)
        return post
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{post_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Delete post",
    description="Delete a post for the authenticated user"
)
async def delete_post(
        post_id: UUID,
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        is_deleted = await delete_post_service(db, post_id, user.get("user_id"))
        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post not found")

        return {"message": "Post deleted successfully", "id":post_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))