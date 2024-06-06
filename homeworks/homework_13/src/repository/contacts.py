from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, and_
from sqlalchemy.sql import func
from typing import List
from datetime import date, timedelta

from src.database.models import Contact, User
from src.database.db import get_db
from src.schemas import ContactSchema


async def get_contacts(limit: int, offset: int, user: User, db: AsyncSession) -> List[Contact]:
    query = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(query)
    # contacts = (
    #     db.query(Contact)
    #     .filter_by(user = user)
    #     .offset(offset)
    #     .limit(limit)
    #     .all()
    # )
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession) -> List[Contact]:
    query = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(query)
    # contacts = (
    #     db.query(Contact)
    #     .offset(offset)
    #     .limit(limit)
    #     .all()
    # )
    return contacts.scalars().all()

async def get_contact(contact_id: int, user: User, db: AsyncSession) -> Contact | None:
    query = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(query)
    # contact = (
    #     db.query(Contact)
    #     .filter_by(id = contact_id, user = user)
    #     .first()
    # )
    return contact.scalar_one_or_none()


async def find_contacts(find_str: str, user: User, db: AsyncSession) -> List[Contact] | None:
    query = select(Contact)\
            .filter_by(user=user)\
            .filter(or_(Contact.name.contains(find_str),
                        Contact.surname.contains(find_str),
                        Contact.email.contains(find_str),
                        ))
    contacts = await db.execute(query)
    # contact = (
    #     db.query(Contact)
    #     .filter_by(user = user)
    #     .filter(
    #         or_(
    #             Contact.name.contains(find_str),
    #             Contact.surname.contains(find_str),
    #             Contact.email.contains(find_str),
    #         )
    #     )
    #     .all()
    # )
    return contacts.scalars().all()


async def find_next_days_birthdays(next_days: int, user: User, db: AsyncSession) -> List[Contact]:
    days_list = [
        (date.today() + timedelta(days=delta)).strftime("%m%d")
        for delta in range(0, next_days)
    ]
    query = select(Contact).filter_by(user=user).where(func.to_char(Contact.birthday, 'MMDD').in_(days_list))
    contacts = await db.execute(query)
    # contacts = (
    #     db.query(Contact)
    #     .filter_by(user = user)
    #     .where(func.to_char(Contact.birthday, "MMDD").in_(days_list))
    #     .all()
    # )
    return contacts.scalars().all()


async def create_contact(contact: ContactSchema, user: User, db: AsyncSession) -> Contact:
    new_contact = Contact(**contact.model_dump(exclude_unset = True), user = user)
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact


async def update_contact(contact_id: int, contact: ContactSchema, user: User, db: AsyncSession) -> Contact | None:
    query = select(Contact).filter_by(id = contact_id, user = user)
    res = await db.execute(query)
    upd_contact = res.scalar_one_or_none()
    # upd_contact = (
    #     db.query(Contact)
    #     .filter_by(id = contact_id, user = user)
    #     .first()
    # )
    if upd_contact:
        upd_contact.name = contact.name
        upd_contact.surname = contact.surname
        upd_contact.email = contact.email
        upd_contact.phone = contact.phone
        upd_contact.birthday = contact.birthday
        upd_contact.info = contact.info
        await db.commit()
        await db.refresh(upd_contact)
    return upd_contact


async def delete_contact(contact_id: int, user: User, db: AsyncSession) -> Contact | None:
    query = select(Contact).filter_by(id = contact_id, user = user)
    res = await db.execute(query)
    contact = res.scalar_one_or_none()
    # contact = (
    #     db.query(Contact)
    #     .filter_by(id = contact_id, user = user)
    #     .first()
    # )
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
