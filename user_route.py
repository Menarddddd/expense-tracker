from typing import Annotated, List
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from models import User
from schemas import (
    UserCreate,
    UserCreateResponse,
    UserResponse,
    UserUpdate,
    AccessToken,
)
from security import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter()


@router.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)

    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
        )

    access_token = create_access_token({"sub": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    form_data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist"
        )

    hashed_password = hash_password(form_data.password)

    new_user = User(
        first_name=form_data.username,
        last_name=form_data.last_name,
        username=form_data.username,
        password=hashed_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_user(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    stmt = select(User).options(selectinload(User.trackers))
    result = await db.execute(stmt)
    users = result.scalars().all()

    return users


@router.patch("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_profile(
    form_data: UserUpdate, db: Annotated[AsyncSession, Depends(get_db)]
):
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist"
        )

    update_user = form_data.model_dump(exclude_unset=True)

    for key, value in update_user.items():
        pass
