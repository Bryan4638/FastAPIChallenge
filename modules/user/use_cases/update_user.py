from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash
from modules.auth.model.model import UserModel
from modules.user.dto.update_user_dto import UpdateUserDTO


class UpdateUser:
    @classmethod
    async def update_user(
        cls,
        db: AsyncSession,
        user: UserModel,
        update_data: UpdateUserDTO
    ) -> Optional[UserModel]:

        try:

            if update_data.last_name is not None:
                user.last_name = update_data.last_name
            if update_data.first_name is not None:
                user.first_name = update_data.first_name
            if update_data.password is not None:
                user.password = get_password_hash(update_data.password)


            db.add(user)
            await db.commit()
            await db.refresh(user)

            return user

        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error while updating user: {str(e)}")
        except Exception as e:
            await db.rollback()
            raise ValueError(f"Error updating user: {str(e)}")