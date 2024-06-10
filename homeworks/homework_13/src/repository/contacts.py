from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from typing import List
from datetime import date, timedelta

from src.database.models import Contact, User
from src.schemas import ContactSchema


async def get_contacts(
    limit: int, offset: int, user: User, db: AsyncSession
) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of contacts to skip
    :param user: User: Filter the contacts by user
    :param db: AsyncSession: Pass in the database session
    :return: A list of contacts
    :doc-author: Trelent
    """
    query = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession) -> List[Contact]:
    """
    The get_all_contacts function returns a list of all contacts in the database.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify how many records to skip before returning the results
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    query = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def get_contact(contact_id: int, user: User, db: AsyncSession) -> Contact | None:
    """
    The get_contact function returns a contact object from the database.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param user: User: Filter the query by user
    :param db: AsyncSession: Pass the database session to the function
    :return: A contact object or none
    :doc-author: Trelent
    """
    query = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(query)
    return contact.scalar_one_or_none()


async def find_contacts(
    find_str: str, user: User, db: AsyncSession
) -> List[Contact] | None:
    """
    The find_contacts function takes a string, user and database session as arguments.
    It then queries the database for contacts that match the find_str argument in either their name, surname or email fields.
    The function returns a list of matching contacts.

    :param find_str: str: Search for a string in the database
    :param user: User: Filter the contacts by user
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    query = (
        select(Contact)
        .filter_by(user=user)
        .filter(
            or_(
                Contact.name.contains(find_str),
                Contact.surname.contains(find_str),
                Contact.email.contains(find_str),
            )
        )
    )
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def find_next_days_birthdays(
    next_days: int, user: User, db: AsyncSession
) -> List[Contact]:
    """
    The find_next_days_birthdays function returns a list of contacts whose birthdays are within the next `next_days` days.

    :param next_days: int: Determine how many days in the future to look for birthdays
    :param user: User: Filter the contacts by user
    :param db: AsyncSession: Pass the database connection to the function
    :return: A list of contacts whose birthday is in the next n days
    :doc-author: Trelent
    """
    days_list = [
        (date.today() + timedelta(days=delta)).strftime("%m%d")
        for delta in range(0, next_days)
    ]
    query = (
        select(Contact)
        .filter_by(user=user)
        .where(func.to_char(Contact.birthday, "MMDD").in_(days_list))
    )
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def create_contact(
    contact: ContactSchema, user: User, db: AsyncSession
) -> Contact:
    """
    The create_contact function creates a new contact in the database.

    Args:
        contact (ContactSchema): The ContactSchema object to be created.
        user (User): The User object that owns the Contact being created.
        db (AsyncSession): An async SQLAlchemy session for interacting with the database.  This is provided by FastAPI's dependency injection system, and should not be passed in manually by users of this function!  It is used to commit changes made to the database and refresh objects after they have been committed so that their primary keys are populated correctly.

    :param contact: ContactSchema: Pass in the contact data that is being created
    :param user: User: Get the user id from the token
    :param db: AsyncSession: Create a new contact in the database
    :return: A contact object
    :doc-author: Trelent
    """
    new_contact = Contact(**contact.model_dump(exclude_unset=True), user=user)
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact


async def update_contact(
    contact_id: int, contact: ContactSchema, user: User, db: AsyncSession
) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            user (User): The user who owns the contacts to update.
            db (AsyncSession): An async session for interacting with an SQLAlchemy database engine.

    :param contact_id: int: Identify the contact that is to be updated
    :param contact: ContactSchema: Get the data from the request body
    :param user: User: Check that the user is logged in and has access to this contact
    :param db: AsyncSession: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    query = select(Contact).filter_by(id=contact_id, user=user)
    res = await db.execute(query)
    upd_contact = res.scalar_one_or_none()
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


async def delete_contact(
    contact_id: int, user: User, db: AsyncSession
) -> Contact | None:
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: int: Specify which contact to delete
    :param user: User: Get the user from the database
    :param db: AsyncSession: Pass the database session to the function
    :return: A contact object if the contact was deleted successfully
    :doc-author: Trelent
    """
    query = select(Contact).filter_by(id=contact_id, user=user)
    res = await db.execute(query)
    contact = res.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
