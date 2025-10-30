from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime

from modules.auth.dto.register_dto import RegisterDTO
from modules.auth.model.model import UserModel
from modules.auth.utils.helper import get_password_hash


class CreateUser:
    @staticmethod
    async def create_user(db: AsyncSession, user_data: RegisterDTO) -> UserModel:
        try:
            hashed_password = get_password_hash(user_data.password)

            new_user = UserModel(
                id=uuid4(),
                username=user_data.username,
                password=hashed_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_deleted=False
            )

            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            return new_user
        except IntegrityError:
            await db.rollback()
            raise ValueError("Username already exists or constraint violation")
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error: {str(e)}")