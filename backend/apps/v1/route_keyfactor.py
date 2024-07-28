from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.contactus import create_new_contact
from schemas.contactus import ContactCreate

router = APIRouter()

# Set up Jinja2Templates
templates = Jinja2Templates(directory="template1")

@router.get("/keyfactor")
async def get_keyfactor(request: Request):
    # Render the template
    return templates.TemplateResponse("keyfactor.html", {"request": request})

@router.post("/keyfactor", response_class=HTMLResponse)
async def submit_keyfactor_form(
    request: Request,
    db: Session = Depends(get_db),
    course: str = Form(...),
    customer_name: str = Form(...),
    customer_phone: int = Form(...),
    text: str = Form(...)
):
    contact_data = ContactCreate(branch=course, name=customer_name, phone_no=customer_phone, message=text)
    try:
        contact = create_new_contact(contact=contact_data, db=db)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(repr(e))
        return templates.TemplateResponse(
            "keyfactor.html",
            {"request": request, "error_message": "An error occurred while submitting your information"}
        )