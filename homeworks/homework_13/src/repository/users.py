from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserSchema

async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)) -> User:
    query = select(User).filter_by(email=email)
    user = await db.execute(query)
    user = user.scalar_one_or_none()
    return user
    # return db.query(User).filter(User.email == email).first()

async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)) -> User:
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()

async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user