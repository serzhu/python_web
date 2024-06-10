from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.roles import RoleAccess
from src.database.db import get_db
from src.database.models import Role, User
from src.schemas import ContactSchema, ContactsAllResponseSchema
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix="/contacts", tags=["contacts"])
access_to_route_all = RoleAccess([Role.ADMIN])


@router.get(
    "/",
    response_model=list[ContactsAllResponseSchema],
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def get_contacts(
    limit: int = Query(10),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contacts function returns a list of contacts for the current user.
        The limit and offset parameters are used to paginate the results.


    :param limit: int: Limit the number of contacts returned
    :param offset: int: Determine where to start the query
    :param db: AsyncSession: Pass the database session to the repository layer
    :param user: User: Get the user from the database
    :param : Limit the number of contacts returned
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(limit, offset, user, db)
    return contacts


@router.get(
    "/all",
    response_model=list[ContactsAllResponseSchema],
    dependencies=[
        Depends(access_to_route_all),
        Depends(RateLimiter(times=1, seconds=10)),
    ],
)
async def get_all_contacts(
    limit: int = Query(10),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The get_all_contacts function returns all contacts in the database.
        The function takes a limit and offset parameter to control how many contacts are returned at once.
        The function also requires an authenticated user.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Skip the first n records
    :param db: AsyncSession: Pass the database session into the function
    :param user: User: Get the current user
    :param : Limit the number of contacts returned
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_all_contacts(limit, offset, db)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactSchema,
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contact function returns a contact by its id.

    :param contact_id: int: Get the contact_id from the url
    :param db: AsyncSession: Pass the database session to the repository layer
    :param user: User: Get the current user from the auth_service
    :param : Get the contact id from the url
    :return: A contact object, but the schema expects a list of contacts
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get(
    "/find/",
    response_model=list[ContactSchema],
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def find_contact(
    find_str: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The find_contact function is used to find a contact by name.
        The function will return all contacts that match the search string.
        If no contacts are found, an HTTP 404 error will be returned.

    :param find_str: str: Find the contact in the database
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user from the database
    :param : Pass the database connection to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.find_contacts(find_str, user, db)
    if len(contacts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contacts


@router.get(
    "/next_days_birthdays/",
    response_model=list[ContactSchema],
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
)
async def find_next_days_birthdays(
    next_days: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The find_next_days_birthdays function returns a list of contacts that have birthdays in the next X days.
        Args:
            next_days (int): The number of days to look ahead for birthdays.
            db (AsyncSession, optional): An async database session object. Defaults to Depends(get_db).
            user (User, optional): A User object containing information about the current user's identity and permissions. Defaults to Depends(auth_service.get_current_user).

    :param next_days: int: Specify how many days in the future we want to get birthdays for
    :param db: AsyncSession: Get the database session
    :param user: User: Get the current user from the database
    :param : Get the number of days to look for birthdays
    :return: The following:
    :doc-author: Trelent
    """
    contacts = await repository_contacts.find_next_days_birthdays(next_days, user, db)
    print(contacts)
    if len(contacts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contacts


@router.post(
    "/",
    response_model=ContactSchema,
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    body: ContactSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactSchema object as input, and returns the newly created contact.


    :param body: ContactSchema: Validate the body of the request
    :param db: AsyncSession: Pass the database session to the repository
    :param user: User: Get the user from the auth_service
    :param : Get the current user
    :return: An object of type contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, user, db)
    return contact


@router.put(
    "/{contact_id}",
    response_model=ContactSchema,
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def update_contact(
    contact_id: int,
    body: ContactSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactSchema): The updated Contact object to be stored in the database.
            db (AsyncSession, optional): An async session for interacting with an async database driver such as Asyncpg or Motor/MongoDB. Defaults to Depends(get_db).
            user (User, optional): A User object containing information about the currently logged-in user making this request. Defaults to Depends(auth_service.get_

    :param contact_id: int: Identify the contact that will be updated
    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the repository layer
    :param user: User: Get the current user
    :param : Get the contact id,
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete(
    "/{contact_id}",
    response_model=ContactSchema,
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            db (AsyncSession, optional): An async session for interacting with the database. Defaults to Depends(get_db).
            user (User, optional): A User object representing an authenticated user making this request. Defaults to Depends(auth_service.get_current_user).

    :param contact_id: int: Specify the id of the contact to delete
    :param db: AsyncSession: Pass the database connection to the repository layer
    :param user: User: Get the current user from the auth_service
    :param : Get the contact id from the url
    :return: A contact object, which is a dict
    :doc-author: Trelent
    """
    contact = await repository_contacts.delete_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
