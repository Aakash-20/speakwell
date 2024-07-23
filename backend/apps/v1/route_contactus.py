from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.contactus import create_new_contact
from schemas.contactus import ContactCreate, ShowContact

router = APIRouter()
templates = Jinja2Templates(directory="template")

@router.get("/contact", response_class=HTMLResponse)
async def get_contact_form(request: Request):
    return templates.TemplateResponse("contactUs.html", {"request": request})

@router.post("/contact", response_class=HTMLResponse)
async def submit_contact_form(
    request: Request,
    db: Session = Depends(get_db),
    branch: str = Form(...),
    name: str = Form(...),
    phone_no: int = Form(...),
    message: str = Form(...)
):
    contact_data = ContactCreate(branch=branch, name=name, phone_no=phone_no, message=message)
    try:
        contact = create_new_contact(contact=contact_data, db=db)
        return templates.TemplateResponse(
            "contactUs.html",
            {"request": request, "success_message": "Contact information submitted successfully"}
        )
    except Exception as e:
        print(repr(e))
        return templates.TemplateResponse(
            "contactUs.html",
            {"request": request, "error_message": "An error occurred while submitting your information"}
        )