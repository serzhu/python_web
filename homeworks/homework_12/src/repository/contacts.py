from fastapi import Depends
from sqlalchemy import or_, and_
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from src.database.models import Contact, User
from src.database.db import get_db
from src.schemas import ContactSchema


def get_contacts(
        limit: int, offset: int, user: User, db: Session) -> List[Contact]:
    contacts = (
        db.query(Contact)
        .filter_by(user = user)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return contacts


def get_all_contacts(
        limit: int, offset: int, db: Session) -> List[Contact]:
    contacts = (
        db.query(Contact)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return contacts

def get_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = (
        db.query(Contact)
        .filter_by(id = contact_id, user = user)
        .first()
    )
    return contact


def find_contact(find_str: str, user: User, db: Session) -> List[Contact] | None:
    contact = (
        db.query(Contact)
        .filter_by(user = user)
        .filter(
            or_(
                Contact.name.contains(find_str),
                Contact.surname.contains(find_str),
                Contact.email.contains(find_str),
            )
        )
        .all()
    )
    return contact


def find_next_days_birthdays(next_days: int, user: User, db: Session) -> List[Contact] | None:
    days_list = [
        (date.today() + timedelta(days=delta)).strftime("%m%d")
        for delta in range(0, next_days)
    ]
    contacts = (
        db.query(Contact)
        .filter_by(user = user)
        .where(func.to_char(Contact.birthday, "MMDD").in_(days_list))
        .all()
    )
    return contacts


def create_contact(contact: ContactSchema, user: User, db: Session = Depends(get_db)) -> Contact:
    new_contact = Contact(
        **contact.model_dump(exclude_unset = True), user = user
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def update_contact(contact_id: int, contact: ContactSchema, user: User, db: Session = Depends(get_db)) -> Contact | None:
    upd_contact = (
        db.query(Contact)
        .filter_by(id = contact_id, user = user)
        .first()
    )
    if upd_contact:
        upd_contact.name = contact.name
        upd_contact.surname = contact.surname
        upd_contact.email = contact.email
        upd_contact.phone = contact.phone
        upd_contact.birthday = contact.birthday
        upd_contact.info = contact.info
        db.commit()
        db.refresh(upd_contact)
    return upd_contact


def delete_contact(contact_id: int, user: User, db: Session = Depends(get_db)) -> Contact | None:
    contact = (
        db.query(Contact)
        .filter_by(id = contact_id, user = user)
        .first()
    )
    if contact:
        db.delete(contact)
        db.commit()
    return contact
