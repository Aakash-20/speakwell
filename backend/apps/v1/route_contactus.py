import json
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi import responses, status, Form
from sqlalchemy.orm import Session
from schemas.contactus import ContactCreate
from db.session import get_db
from db.repository.contactus import create_new_contact
from pydantic.error_wrappers import ValidationError

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.post("/contactus")
def contactus(request: Request,
    name: str = Form(...),
    phone_no: str = Form(...),
    message: str = Form(...),
    branch: str = Form(...),
    db: Session = Depends(get_db)):
    errors = []
    try:
        contact = ContactCreate(name=name, phone_no=phone_no, message=message, branch=branch)
        create_new_contact(contact=contact, db=db)
        return responses.RedirectResponse("/?alert=Message%20Sent%20Successfully", status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        errors_list = json.loads(e.json())
        for item in errors_list:
            errors.append(item.get("loc")[0] + ": " + item.get("msg"))
        return templates.TemplateResponse("contactUs.html", {"request": request, "errors": errors})