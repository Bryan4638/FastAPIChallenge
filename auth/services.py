from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from auth.DTO.auth_response_dto import AuthResponseDTO, UserResponse
from auth.DTO.register_dto import RegisterDTO
from auth.use_cases.create_user import CreateUser
from auth.use_cases.find_user import get_by_username
from auth.utils.helper import verify_password, create_access_token


async def authenticate_user(db: AsyncSession,
        username: str,
        password: str
) -> Optional[AuthResponseDTO]:

    user = await get_by_username(db=db, username=username)

    if not user:
        return None

    if user.is_deleted:
        return None

    if not verify_password(password, user.password):
        return None

    access_token = create_access_token(data={"sub": user.username, "user_id": str(user.id)})

    user_response = UserResponse(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at
    )

    auth_response = AuthResponseDTO(user=user_response, access_token=access_token)

    return auth_response


async def register_user(db: AsyncSession, user_data: RegisterDTO) -> UserResponse:

    existing_user = await get_by_username(db=db, username=user_data.username)

    if existing_user:
        raise ValueError("The username is already registered")

    user = await CreateUser.create_user(db, user_data)

    user_response = UserResponse(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at
    )

    return user_response
