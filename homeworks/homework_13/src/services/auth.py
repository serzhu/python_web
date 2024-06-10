import os
from datetime import datetime, timedelta, UTC
from typing import Optional

# from dotenv import load_dotenv
from pathlib import Path

import redis
import pickle
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.database.db import get_db
from src.repository import users as repositories_users
from src.conf.config import settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    cache = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and the hashed version of that password,
            and returns True if they match, False otherwise. This is used to verify that the user's login
            credentials are correct.

        :param self: Represent the instance of the class
        :param plain_password: Compare the password entered by the user with that stored in the database
        :param hashed_password: Compare the hashed password in the database with the plain text password entered by user
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
            The function uses the pwd_context object to generate a hash from the given password.

        :param self: Represent the instance of the class
        :param password: str: Pass in the password that is to be hashed
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        The create_access_token function creates a new access token.


        :param self: Represent the instance of the class
        :param data: dict: Pass in the data that you want to encode into your token
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: An encoded jwt
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.now(UTC), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): The data to be encoded in the JWT. This should include at least a &quot;sub&quot; key, which is the subject of this token, and will usually be a user ID of some kind.
                expires_delta (Optional[float]): A timedelta object representing how long until this token expires. If not provided, it defaults to 7 days from now.

        :param self: Represent the instance of the class
        :param data: dict: Pass the user data to the function
        :param expires_delta: Optional[float]: Set the expiration time of the refresh token
        :return: A token that is used to refresh the access token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(UTC) + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.now(UTC), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
            The function will raise an HTTPException if the token is invalid or has expired.
            If the token is valid, it will return a string with the email address of
            user who owns that refresh_token.

        :param self: Represent the instance of the class
        :param refresh_token: str: Pass the refresh token to the function
        :return: The email of the user
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        """
        The get_current_user function is a dependency that will be called by the FastAPI framework to retrieve the current user.
        It uses the token from the Authorization header and validates it against our JWT secret key. If successful, it returns a User object.

        :param self: Represent the instance of a class
        :param token: str: Get the token from the authorization header
        :param db: AsyncSession: Get the database session
        :return: A user object
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        user_hash = str(email)
        user = self.cache.get(user_hash)
        if user is None:
            print("from Database")
            user = await repositories_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.cache.set(user_hash, pickle.dumps(user))
            self.cache.expire(user_hash, 300)
        else:
            print("from Cache")
            user = pickle.loads(user)
        return user

    async def create_email_token(self, data: dict):
        """
        The create_email_token function creates a JWT token that is used to verify the user's email address.
            The token contains the following data:
                - iat (issued at): The time when the token was created.
                - exp (expiration): When this token expires, 7 days from now.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the data we want to encode
        :return: A token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(UTC), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        The function first decodes the token using jwt.decode, which is part of PyJWT, a Python library for encoding and decoding JSON Web Tokens (JWTs).
        If successful, it will return the email address associated with that JWT.

        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :return: The email that was encoded in the token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )


auth_service = Auth()
