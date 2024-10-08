from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, status
from fastapi.responses import RedirectResponse 
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from schemas.blog import CreateBlog
from db.repository.blog import create_new_blog, delete_blog_by_id, retrieve_blog
from db.repository.admin import is_admin
from db.session import get_db
from api.v1.route_login import get_current_user
import os
from fastapi.security.utils import get_authorization_scheme_param


templates = Jinja2Templates(directory="template")
router = APIRouter()


UPLOAD_DIR = "template/blog/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/admin/create-blog")
async def create_blog_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")
    scheme, token = get_authorization_scheme_param(token)
    try:
        current_user = get_current_user(token=token, db=db)
        
        if not is_admin(current_user.id):
            return RedirectResponse(
                url="/admin_index?message=You do not have permission to create blog posts",
                status_code=status.HTTP_303_SEE_OTHER)

        image_url = None
        if file:
            image_data = await file.read()
            image_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(image_path, "wb") as f:
                f.write(image_data)
            image_url = f"{request.base_url}blogs_image/{file.filename}"

        blog = CreateBlog(title=title, content=content)
        new_blog = create_new_blog(blog=blog, db=db, author_id=current_user.id, image_url=image_url)
        
        return RedirectResponse(url="/admin_index?message=Blog created successfully", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Error creating blog: {str(e)}")
        errors = ["An error occurred while creating the blog"]
        if "Could not validate credentials" in str(e):
            errors = ["Please log in to create a blog"]
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "errors": errors, "title": title, "content": content},
        )


@router.get("/delete/{id}")
def delete_a_blog(request: Request, id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        author = get_current_user(token=token, db=db)
        msg = delete_blog_by_id(id=id, author_id=author.id, db=db)
        alert = msg.get("error") or msg.get("msg")
        return RedirectResponse(
            f"/admin_index?alert={alert}", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print(f"Exception raised while deleting {e}")
        blog = retrieve_blog(id=id, db=db)
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "alert": "Please Login Again", "blog": blog})
    

