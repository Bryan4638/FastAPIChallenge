from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from modules.auth.model.model import UserModel
from sqlalchemy import select

class FindUser:
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> UserModel | None:
        try:
            query = select(UserModel).where(UserModel.username == username)

            result = await db.execute(query)

            return result.scalar_one_or_none()

        except IntegrityError:
            await db.rollback()
            raise ValueError("The username does not exist")
        except SQLAlchemyError as e:
            await db.rollback()
            raise ValueError(f"Database error: {str(e)}")