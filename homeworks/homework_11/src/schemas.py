from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from pydantic_extra_types.phone_numbers import PhoneNumber

class ContactSchema(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    surname: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(max_length=30)
    phone: PhoneNumber
    birthday: date 
    info: Optional[str] = Field(min_length=2, max_length=100)