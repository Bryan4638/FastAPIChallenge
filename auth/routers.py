from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from auth.DTO.auth_response_dto import AuthResponseDTO, RegisterResponseDTO
from auth.DTO.register_dto import RegisterDTO
from auth.services import register_user, authenticate_user
from core.config import settings
from core.database import get_session


# Router
router = APIRouter(
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register",
    response_model=RegisterResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register new user"
)
async def register(
        user_data: RegisterDTO,
        db: AsyncSession = Depends(get_session)
):
    try:
        response = await register_user(db, user_data)
        return {"message": "Client successfully created ", "response": response }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login",
    response_model=AuthResponseDTO,
    summary="Login user",
    description="Authenticate user with username and password, return JWT token"
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_session)
):
    token = await authenticate_user(db, form_data.username, form_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
