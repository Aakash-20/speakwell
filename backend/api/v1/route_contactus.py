from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.contactus import ContactCreate, ShowContact
from db.session import get_db
from db.repository.contactus import create_new_contact

router = APIRouter()


@router.post("/contacts/", response_model=ShowContact, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        contact = create_new_contact(contact=contact, db=db)
        print(contact)
        return contact
    except Exception as e:
            print(repr(e))
