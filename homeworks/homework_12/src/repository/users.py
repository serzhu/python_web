from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserSchema

def get_user_by_email(email, db: Session = Depends(get_db())) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(body: UserSchema, db: Session = Depends(get_db())) -> User:
    new_user = User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()

