from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.database.models import Role


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=8)
    email: EmailStr


class UserResponseSchema(BaseModel):
    id: int = 1
    username: str
    email: EmailStr
    avatar: str
    role: Role

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactSchema(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    surname: str = Field(min_length=3, max_length=20)
    email: EmailStr
    phone: PhoneNumber
    birthday: date
    info: Optional[str] = Field(min_length=2, max_length=100)

    class Config:
        from_attributes = True


class ContactsAllResponseSchema(ContactSchema):
    id: int = 1
    user: UserResponseSchema

    class Config:
        from_attributes = True


class RequestEmail(BaseModel):
    email: EmailStr
