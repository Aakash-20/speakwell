from sqlalchemy.orm import Session
from sqlalchemy import desc
from schemas.enquiry import CreateEnquiry
from db.models.enquiry import Enquiry


def create_new_enquiry(enquiry: CreateEnquiry, db: Session):
    new_enquiry = Enquiry(
        course=enquiry.course,
        customer_name=enquiry.customer_name,
        customer_phone=enquiry.customer_phone,
        text=enquiry.text,
    )
    db.add(new_enquiry)
    db.commit()
    db.refresh(new_enquiry)
    return new_enquiry


def retrieve_enquiry(id: int, db: Session):
    blog = db.query(Enquiry).filter(Enquiry.id == id).first()
    return blog


def list_all_enquiry(db: Session):
    enquiry = db.query(Enquiry).order_by(desc(Enquiry.created_at)).all()
    return enquiry