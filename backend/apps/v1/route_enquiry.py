from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.enquiry import create_new_enquiry
from schemas.enquiry import CreateEnquiry

router = APIRouter()
templates = Jinja2Templates(directory="template1")

@router.get("/enquiry", response_class=HTMLResponse)
async def get_enquiry_form(request: Request):
    return templates.TemplateResponse("keyfactor.html", {"request": request})

@router.post("/enquiry", response_class=HTMLResponse)
async def submit_enquiry_form(
    request: Request,
    db: Session = Depends(get_db),
     course: str = Form(...),
    customer_name: str = Form(...),
    customer_phone: int = Form(...),
    text: str = Form(...)
    
):
    enquiry_data = CreateEnquiry(course=course, customer_name=customer_name, customer_phone=customer_phone, text=text)
    try:
        enquiry = create_new_enquiry(enquiry=enquiry_data, db=db)
        return templates.TemplateResponse(
            "keyfactor.html",
            {"request": request, "success_message": "Enquiry submitted successfully"}
        )
    except Exception as e:
        print(repr(e))
        return templates.TemplateResponse(
            "keyfactor.html",
            {"request": request, "error_message": "An error occurred while submitting your enquiry"}
        )
