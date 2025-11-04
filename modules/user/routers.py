from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from core.config import settings
from core.database import get_session
from core.security import decode_token
from modules.user.dto.delete_response_dto import DeleteResponseDTO

from modules.user.dto.update_user_dto import UpdateUserDTO
from modules.user.dto.user_response_dto import UserResponseDTO
from modules.user.service.service import update_user_service, delete_user_service

# Router
router = APIRouter(
    prefix=f"{settings.API_V1_STR}/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.put("/{user_id}",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Update user",
    description="Update user authenticated"
)
async def update_user(
        update_data: UpdateUserDTO,
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        user = await update_user_service(db, user.get("user_id"), update_data)

        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}",
    response_model=DeleteResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Delete user",
    description="Delete user authenticated"
)
async def delete_user(
        user: Annotated[dict, Depends(decode_token)],
        db: AsyncSession = Depends(get_session)
):
    try:
        is_deleted = await delete_user_service(db, user.get("user_id"))

        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

        return {"message": "User deleted successfully", "id":user.get("user_id")}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))