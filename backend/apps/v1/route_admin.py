from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.repository.admin import get_current_user
from db.repository.blog import list_blogs
from db.repository.image import get_all_images
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.address import list_addresses
from db.repository.url import get_url_by_id


templates = Jinja2Templates(directory="template")
router = APIRouter()


@router.get("/admin_index")
def admin_home(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        blogs = list_blogs(db=db)
        return templates.TemplateResponse("admin_index.html", {"request": request, "blogs": blogs})
    except Exception as e:
        print(f"Error retrieving blogs: {str(e)}")
        return templates.TemplateResponse("admin_index.html", {"request": request, "blogs": [], "message": f"Error retrieving blogs: {str(e)}"})


@router.get("/admin_image", response_class=HTMLResponse)
async def fetch_all_images(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    images = get_all_images(db=db)
    return templates.TemplateResponse("admin_image.html", {"request": request, "images": images})


@router.get("/admin_contact", response_class=HTMLResponse)
async def fetch_contactus(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    addresses = list_addresses(db=db)
    return templates.TemplateResponse("admin_contactus.html", {"request": request, "addresses": addresses})


@router.get("/admin_review", response_class=HTMLResponse)
async def admin_review(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    url = get_url_by_id(db=db, url_id=1)
    return templates.TemplateResponse("admin_review.html", {"request": request, "widget": url.url})