from fastapi import Request, APIRouter, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from db.repository.login import get_user_by_email
from fastapi.security.utils import get_authorization_scheme_param
from db.repository.blog import list_blogs
from db.repository.image import get_all_images
from sqlalchemy.orm import Session
from db.session import get_db
from core.config import settings
from jose import jwt, JWTError
from db.repository.address import create_new_address, list_addresses, remove_address


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


@router.get("/admin_image", response_class=HTMLResponse)
async def fetch_all_images(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    images = get_all_images(db=db)
    return templates.TemplateResponse("admin_image.html", {"request": request, "images": images})


@router.get("/admin_contact", response_class=HTMLResponse)
async def fetch_contactus(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    addresses = list_addresses(db=db)
    return templates.TemplateResponse("admin_contactus.html", {"request": request, "addresses": addresses})


@router.get("/admin_review", response_class=HTMLResponse)
async def fetch_review(request: Request,  user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("admin_review.html", {"request": request})
