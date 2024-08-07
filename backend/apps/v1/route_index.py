from fastapi import Request, Form, Query, APIRouter, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.image import get_all_images_logic
from db.repository.blog import list_blogs


templates = Jinja2Templates(directory="template")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_blogs(request: Request, db: Session = Depends(get_db)):
    try:
        blogs = list_blogs(db=db)
        blog_list = [
            {
                "id": blog.id,
                "image": blog.image,
                "title": blog.title,
                "content": blog.content
            }
            for blog in blogs
        ]
        return templates.TemplateResponse("index.html", {"request": request, "blogs": blog_list})
    except Exception as e:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": f"Error retrieving blogs: {str(e)}"}
        )


@router.get("/aboutUs", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("aboutUs.html", {"request": request, "message": "success"})


@router.get("/footer")
async def get_footer(request: Request):
    return templates.TemplateResponse("footer.html", {"request": request})


@router.get("/keyfactor")
async def get_keyfactor(request: Request):
    return templates.TemplateResponse("keyfactor.html", {"request": request})


@router.get("/header")
async def get_header(request: Request):
    return templates.TemplateResponse("header.html", {"request": request})


@router.get("/whatsapp", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("whatsapp.html", {"request": request, "message": "success"})


@router.get("/gallery")
async def read_images(request: Request, db: Session = Depends(get_db)):
    images = await get_all_images_logic(request, db)
    return templates.TemplateResponse("gallery.html", {"request": request, "images": images})


@router.get("/why_us")
async def get_why_us(request: Request):
    return templates.TemplateResponse("whyUs.html", {"request": request})




