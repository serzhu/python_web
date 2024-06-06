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
    contact = await repository_contacts.delete_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
