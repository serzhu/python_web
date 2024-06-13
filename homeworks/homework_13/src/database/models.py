import enum
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    func,
    Enum,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column("Name", String(20), nullable=False)
    surname = Column("Surname", String(20), nullable=False)
    phone = Column("Phone", String(20), nullable=False, unique=True)
    email = Column("Email", String(30), nullable=False, unique=True)
    birthday = Column("Birthday", Date, nullable=False)
    info = Column("Additional_info", String(100))
    created_at = Column("created_at", DateTime, default=func.now())
    updated_at = Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    user_id = Column("User_id", Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="contacts", lazy="joined")


class Role(enum.Enum):
    ADMIN: str = "admin"
    USER: str = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column("Login", String(255), nullable=False, unique=True)
    password = Column("Password", String(255), nullable=False)
    email = Column("Email", String(255), nullable=False, unique=True)
    avatar = Column("Avatar", String(255), nullable=True)
    refresh_token = Column("Refresh_Token", String(255))
    created_at = Column("created_at", DateTime, nullable=False, default=func.now())
    updated_at = Column("updated_at", DateTime, nullable=False, default=func.now(), onupdate=func.now())
    role = Column("Role", Enum(Role), default=Role.USER, nullable=True)
    confirmed = Column(Boolean, default=False)
