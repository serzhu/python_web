from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column('Name', String(20), nullable=False)
    surname = Column('Surname', String(20), nullable=False)
    phone = Column('Phone', String(20), nullable=False, unique=True)
    email = Column('Email', String(30), nullable=False, unique=True)
    birthday = Column('Birthday', Date, nullable=False)
    info = Column('Additional_info', String(100))
