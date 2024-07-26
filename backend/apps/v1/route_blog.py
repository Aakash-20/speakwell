from fastapi import APIRouter, Request, Depends
from typing import Optional
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.repository.blog import list_blogs, retrieve_blog, create_new_blog
from db.session import get_db

templates = Jinja2Templates(directory="template")
router = APIRouter()

@router.get("/blog")
def blog_detail(request: Request, id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    return templates.TemplateResponse(
        "blog.html", {"request": request, "blog": blog}
    )

@router.get("/blog2")
def home(request: Request,alert: Optional[str] = None, db: Session = Depends(get_db)):
    blogs = list_blogs(db=db)
    return templates.TemplateResponse(
        "blog2.html", {"request": request, "blogs": blogs,"alert":alert}
    )

