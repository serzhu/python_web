from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)) -> User:
    """
    The get_user_by_email function takes an email and returns the user associated with that email.
        If no user is found, it will return None.

    :param email: str: Specify the email of the user we want to retrieve
    :param db: AsyncSession: Pass in the database session
    :return: A user object, or none if the user does not exist
    :doc-author: Trelent
    """
    query = select(User).filter_by(email=email)
    user = await db.execute(query)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: UserSchema: Validate the request body and convert it into a user object
    :param db: AsyncSession: Pass in the database session
    :return: A user object
    :doc-author: Trelent
    """
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Get the user object from the database
    :param token: str | None: Update the user's refresh token
    :param db: AsyncSession: Commit the changes to the database
    :return: None, so the return type should be none
    :doc-author: Trelent
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function marks a user as confirmed in the database.

    :param email: str: Get the email of the user
    :param db: AsyncSession: Pass in the database session
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    The update_avatar_url function updates the avatar url of a user.

    :param email: str: Find the user in the database
    :param url: str | None: Set the avatar url of a user
    :param db: AsyncSession: Pass the database connection to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
