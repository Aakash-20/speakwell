from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from db.repository.contactus import get_all_contacts
from db.repository.enquiry import list_all_enquiry
from db.repository.blog import list_blogs
from db.repository.image import get_all_images
from sqlalchemy.orm import Session
from db.session import get_db


templates = Jinja2Templates(directory="template")
router = APIRouter()


@router.get("/admin_index")
def admin_home(request: Request, message: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        blogs = list_blogs(db=db)
        return templates.TemplateResponse(
            "admin_index.html", {"request": request, "blogs": blogs, "message": message}
        )
    except Exception as e:
        print(f"Error retrieving blogs: {str(e)}")
        return templates.TemplateResponse(
            "admin_index.html", {"request": request, "blogs": [], "message": f"Error retrieving blogs: {str(e)}"}
        )


@router.get("/admin/enquiry", response_class=HTMLResponse)
async def list_enquiry(request: Request, db: Session = Depends(get_db)):
    enquiry = list_all_enquiry(db)
    return templates.TemplateResponse("admin_enquiry.html", {"request": request, "enquiry": enquiry})


@router.get("/admin/contact", response_class=HTMLResponse)
async def list_contacts(request: Request, db: Session = Depends(get_db)):
    contacts = get_all_contacts(db)
    return templates.TemplateResponse("admin_contact.html", {"request": request, "contacts": contacts})
    

@router.get("/admin_image", response_class=HTMLResponse)
async def fetch_all_images(request: Request, db: Session = Depends(get_db)):
    images = get_all_images(db=db)
    return templates.TemplateResponse("admin_image.html", {"request": request, "images": images})