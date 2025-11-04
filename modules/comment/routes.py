from typing import Annotated, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from core.config import settings
from core.database import get_session
from core.security import decode_token
from modules.comment.dto.request_comment_dto import RequestCommentDTO
from modules.comment.dto.response_comment import ResponseCommentDTO
from modules.comment.service.service import create_comment_service, update_comment_service, delete_comment_service
from modules.user.dto.delete_response_dto import DeleteResponseDTO

# Router
router = APIRouter(
    prefix=f"{settings.API_V1_STR}/comment",
    tags=["comment"],
    responses={404: {"description": "Not found"}},
)


@router.post("/",
    response_model=ResponseCommentDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create comment",
    description="Create a comment for the authenticated user"
)
async def create_comment(
        comment_data: RequestCommentDTO,
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        comment = await create_comment_service(db, comment_data, user.get("user_id"))
        return comment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{comment_id}",
    response_model=Optional[ResponseCommentDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Update comment",
    description="Update a comment for the authenticated user"
)
async def update_comment(
        comment_id: UUID,
        update_data: RequestCommentDTO,
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        comment = await update_comment_service(db, comment_id, user.get("user_id"), update_data)

        return comment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{comment_id}",
    response_model=DeleteResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Delete comment",
    description="Delete a comment for the authenticated user"
)
async def delete_comment(
        comment_id: UUID,
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        is_deleted = await delete_comment_service(db, comment_id, user.get("user_id"))
        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment not found")

        return {"message": "Comment deleted successfully", "id":comment_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))