from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.enquiry import CreateEnquiry, ShowEnquiry
from db.repository.enquiry import create_new_enquiry, retrieve_enquiry, list_all_enquiry

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_enquiry(enquiry: CreateEnquiry, db: Session = Depends(get_db)):
    try:
        enquiry = create_new_enquiry(enquiry=enquiry, db=db)
        print(enquiry)
        return enquiry
    except Exception as e:
            print(repr(e))


@router.get("/{id}", response_model=ShowEnquiry)
def get_enquiry(id: int, db: Session = Depends(get_db)):
    try:
        enquiry = retrieve_enquiry(id=id, db=db)
        if not enquiry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Enquiry with id {id} does not exist")
        return enquiry
    except Exception as e:
            print(repr(e))


@router.get("", response_model=List[ShowEnquiry])
def get_latest_enquiries(db: Session = Depends(get_db)):
    try:
        enquiries = list_all_enquiry(db=db)
        return enquiries
    except Exception as e:
            print(repr(e))