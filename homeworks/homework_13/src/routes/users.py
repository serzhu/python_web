import pickle
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserResponseSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserResponseSchema)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function returns the current user's information.
        ---
        get:
          tags: [users] # This is a tag that can be used to group operations by resources or any other qualifier.
          summary: Returns the current user's information.
          description: Returns the current user's information based on their JWT token in their request header.
          responses: # The possible responses this operation can return, along with descriptions and examples of each response type (if applicable).
            &quot;200&quot;:  # HTTP status code 200 indicates success! In this case, it means we successfully returned a User

    :param current_user: User: Get the current user
    :return: The current user
    :doc-author: Trelent
    """
    return current_user


@router.patch("/avatar", response_model=UserResponseSchema)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    The update_avatar_user function is used to update the avatar of a user.
        The function takes in an UploadFile object, which contains the file that will be uploaded to Cloudinary.
        It also takes in a User object, which is obtained from auth_service.get_current_user(). This function returns
        the current logged-in user's email address and uses it as a key for retrieving their information from Redis cache.
        If no such key exists, then it retrieves their information from PostgreSQL database using repository_users' get() method.

    :param file: UploadFile: Get the file from the request body
    :param current_user: User: Get the current user object from the database
    :param db: AsyncSession: Get the database session from the dependency injection
    :param : Get the current user
    :return: The updated user object
    :doc-author: Trelent
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f"users/{current_user.username}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(f"users/{current_user.username}").build_url(
        width=250, height=250, crop="fill", version=r.get("version")
    )
    user = await repository_users.update_avatar_url(current_user.email, src_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user
