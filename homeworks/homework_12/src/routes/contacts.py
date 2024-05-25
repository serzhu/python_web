from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session


from src.services.roles import RoleAccess
from src.database.db import get_db
from src.database.models import Role, User
from src.schemas import ContactSchema, ContactsAllResponseSchema
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix="/contacts", tags=["contacts"])
access_to_route_all = RoleAccess([Role.ADMIN])

@router.get("/", response_model=list[ContactsAllResponseSchema])
def get_contacts(
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    result = repository_contacts.get_contacts(limit, offset, user, db)
    return result


@router.get("/all", response_model=list[ContactsAllResponseSchema], dependencies=[Depends(access_to_route_all)])
def get_all_contacts(
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    result = repository_contacts.get_all_contacts(limit, offset, db)
    return result

@router.get("/{contact_id}", response_model=ContactSchema)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    result = repository_contacts.get_contact(contact_id, user, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result


@router.get("/find/", response_model=list[ContactSchema])
def find_contact(
    find_str: str,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    result = repository_contacts.find_contact(find_str, user, db)
    if not len(result):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result


@router.get("/next_days_birthdays/", response_model=list[ContactSchema])
def find_next_days_birthdays(
    next_days: int,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    result = repository_contacts.find_next_days_birthdays(next_days, user, db)
    if not len(result):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result


@router.post("/", response_model=ContactSchema, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: ContactSchema,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    result = repository_contacts.create_contact(contact, user, db)
    return result


@router.put("/{contact_id}", response_model=ContactSchema)
def update_contact(
    contact_id: int,
    contact: ContactSchema,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    result = repository_contacts.update_contact(contact_id, contact, user, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result


@router.delete("/{contact_id}", response_model=ContactSchema)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    result = repository_contacts.delete_contact(contact_id, user, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result
