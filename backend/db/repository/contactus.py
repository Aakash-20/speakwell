from sqlalchemy.orm import Session
from db.models.contactus import Contact
from schemas.contactus import ContactCreate

def create_new_contact(contact: ContactCreate, db: Session):
    db_contact = Contact(
                name=contact.name,
                phone_no=contact.phone_no,
                message=contact.message,
                branch=contact.branch,
            )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
