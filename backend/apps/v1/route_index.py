from fastapi import Request, APIRouter, Depends, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.image import get_all_images_logic
from db.repository.blog import list_blogs
from db.repository.url import get_url_by_id
from db.repository.address import list_addresses


templates = Jinja2Templates(directory="template")
router = APIRouter()


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
        url = get_url_by_id(db=db, url_id=1)
        return templates.TemplateResponse("index.html", {"request": request, "blogs": blog_list, "images": images, "widget": url.url})
    except Exception as e:
        print(repr(e))
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": f"Error retrieving blogs: {str(e)}"}
        )


@router.get("/whatsapp", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("whatsapp.html", {"request": request, "message": "success"})


@router.get("/best-spoken-english-classes-in-Nagpur", response_class=HTMLResponse)
async def get_contact_form(request: Request, db: Session = Depends(get_db)):
    addresses = list_addresses(db=db)
    return templates.TemplateResponse("contactUs.html", {"request": request, "addresses": addresses})


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

