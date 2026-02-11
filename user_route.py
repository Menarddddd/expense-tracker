from typing import Annotated, List
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import User
from schemas import UserCreate, UserCreateResponse, UserResponse
from security import hash_password


router = APIRouter()


@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    form_data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    if result:
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
async def get_all_user(db: Annotated[AsyncSession, Depends(get_db)]):
    stmt = select(User).options(selectinload(User.trackers))
    result = await db.execute(stmt)
    users = result.scalars().all()

    return users
