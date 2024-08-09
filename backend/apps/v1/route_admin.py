from fastapi import Request, APIRouter, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from db.repository.login import get_user_by_email
from fastapi.security.utils import get_authorization_scheme_param
from db.repository.contactus import get_all_contacts
from db.repository.enquiry import list_all_enquiry
from db.repository.blog import list_blogs
from db.repository.image import get_all_images
from sqlalchemy.orm import Session
from db.session import get_db
from core.config import settings
from jose import jwt, JWTError

templates = Jinja2Templates(directory="template")
router = APIRouter()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Not authenticated", headers={"Location": "/login"})
    
    scheme, token = get_authorization_scheme_param(token)
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Invalid authentication scheme", headers={"Location": "/login"})

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Not authenticated", headers={"Location": "/login"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Not authenticated", headers={"Location": "/login"})

    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Not authenticated", headers={"Location": "/login"})

    return user

templates = Jinja2Templates(directory="template")
router = APIRouter()

@router.get("/admin_index")
def admin_home(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        blogs = list_blogs(db=db)
        return templates.TemplateResponse(
            "admin_index.html", {"request": request, "blogs": blogs}
        )
    except Exception as e:
        print(f"Error retrieving blogs: {str(e)}")
        return templates.TemplateResponse(
            "admin_index.html", {"request": request, "blogs": [], "message": f"Error retrieving blogs: {str(e)}"}
        )

@router.get("/admin/enquiry", response_class=HTMLResponse)
async def list_enquiry(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    enquiry = list_all_enquiry(db)
    return templates.TemplateResponse("admin_enquiry.html", {"request": request, "enquiry": enquiry})

@router.get("/admin/contact", response_class=HTMLResponse)
async def list_contacts(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    contacts = get_all_contacts(db)
    return templates.TemplateResponse("admin_contact.html", {"request": request, "contacts": contacts})

@router.get("/admin_image", response_class=HTMLResponse)
async def fetch_all_images(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    images = get_all_images(db=db)
    return templates.TemplateResponse("admin_image.html", {"request": request, "images": images})
