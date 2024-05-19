from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.schemas import ContactSchema
from src.repository import contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/")
def get_contacts(limit: int = Query(10), offset: int = Query(0), db: Session = Depends(get_db)):
    result = contacts.get_contacts(limit, offset, db)
    return result


@router.get("/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    result = contacts.get_contact(contact_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result


@router.get("/find/")
def find_contact(find_str: str, db: Session = Depends(get_db)):
    result = contacts.find_contact(find_str, db)
    if not len(result):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result

@router.get("/next_days_birthdays/")
def find_next_days_birthdays(next_days: int, db: Session = Depends(get_db)):
    result = contacts.find_next_days_birthdays(next_days, db)
    if not len(result):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result

@router.post("/")
def create_contact(contact: ContactSchema, db: Session = Depends(get_db)):
    result = contacts.create_contact(contact, db)
    return result


@router.put("/{contact_id}")
def update_contact(contact_id: int, contact: ContactSchema, db: Session = Depends(get_db)):
    result = contacts.update_contact(contact_id, contact, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    result = contacts.delete_contact(contact_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return result
