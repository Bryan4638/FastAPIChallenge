from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from modules.user.dto.update_user_dto import UpdateUserDTO
from modules.user.use_cases.delete_user import DeleteUser
from modules.user.use_cases.find_user_by_id import FindUserById
from modules.user.dto.user_response_dto import UserResponseDTO
from modules.user.use_cases.update_user import UpdateUser


async def delete_user_service(
    db: AsyncSession,
    user_id: UUID
) -> bool:
    try:
        return await DeleteUser.delete_user(db, user_id)
    except Exception as e:
        raise ValueError(f"Error deleting user: {str(e)}")


async def update_user_service(
    db: AsyncSession,
    user_id: UUID,
    update_data: UpdateUserDTO
) -> Optional[UserResponseDTO]:

    user = await FindUserById.get_by_id(db=db, user_id=user_id)

    if not user:
        return None

    if user.is_deleted:
        return None

    updated_user = await UpdateUser.update_user(db, user, update_data)

    return UserResponseDTO(
        id=updated_user.id,
        username=updated_user.username,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
    )