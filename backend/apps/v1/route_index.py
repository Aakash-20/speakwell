from fastapi import Request, Form, Query, APIRouter, Depends, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.image import get_all_images_logic, get_all_images
from db.repository.blog import list_blogs


templates = Jinja2Templates(directory="template")
router = APIRouter()

from fastapi.responses import RedirectResponse

@router.get("/")
async def redirect_to_main():
    return RedirectResponse("/Speakwell/Nagpur/Top-English-Speaking-&-Personality-Development-Classes")


@router.get("/Speakwell/Nagpur/Top-English-Speaking-&-Personality-Development-Classes", response_class=HTMLResponse)
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
        images = await get_all_images_logic(db=db, request=request)

        return templates.TemplateResponse("index.html", {"request": request, "blogs": blog_list, "images": images})
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
    images = await get_all_images_logic(db=db, request=request)
    print(images)
    return templates.TemplateResponse("gallery.html", {"request": request, "images": images})

@router.get("/why_us")
async def get_why_us(request: Request):
    return templates.TemplateResponse("whyUs.html", {"request": request})


@router.get("/contact-us/best-spoken-english-classes-in-Nagpur", response_class=HTMLResponse)
async def get_contact_form(request: Request):
    return templates.TemplateResponse("contactUs.html", {"request": request})


@router.get("/enquiry", response_class=HTMLResponse)
async def get_enquiry_form(request: Request):
    return templates.TemplateResponse("keyfactor.html", {"request": request})


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

