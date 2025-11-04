from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from modules.auth.model.model import UserModel
from sqlalchemy import select

class FindUserById:
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: UUID) -> UserModel | None:
        try:
            query = select(UserModel).where(UserModel.id == user_id)

            result = await db.execute(query)

            return result.scalar_one_or_none()

        except IntegrityError:
            await db.rollback()
            raise ValueError("The user does not exist")
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error: {str(e)}")