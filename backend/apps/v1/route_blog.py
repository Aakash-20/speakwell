from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse 
from typing import Optional
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from schemas.blog import CreateBlog
from db.repository.blog import create_new_blog, delete_blog_by_id, list_blogs, retrieve_blog
from db.session import get_db
from api.v1.route_login import get_current_user
import os


templates = Jinja2Templates(directory="template")
router = APIRouter()


UPLOAD_DIR = "template/blog/images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.get("/blog", response_class=HTMLResponse)
async def read_item(request: Request, message: Optional[str] = None, db: Session = Depends(get_db)):
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
        return templates.TemplateResponse("blog.html", {"request": request, "blogs": blog_list})
    except HTTPException as e:
        return templates.TemplateResponse("error.html", {"request": request, "message": str(e.detail)})
    except Exception as e:
        print(f"Error retrieving blogs: {str(e)}")
        return templates.TemplateResponse(
            "error.html", {"request": request, "message": f"Error retrieving blogs: {str(e)}"}
        )


@router.get("/blog/{id}", response_class=HTMLResponse)
async def read_blog(request: Request, id: int, db: Session = Depends(get_db)):
    try:
        blog = retrieve_blog(db, id)
        print("Blogs:", blog)
        if blog is None:
            raise HTTPException(status_code=404, detail="Blog not found")
        return templates.TemplateResponse("blog2.html", {"request": request, "blog": blog})
    except HTTPException as e:
        return templates.TemplateResponse("error.html", {"request": request, "message": str(e.detail)})
    except Exception as e:
        print(f"Error retrieving blog: {str(e)}")
        return templates.TemplateResponse(
            "error.html", {"request": request, "message": f"Error retrieving blog: {str(e)}"}
        )


@router.get("/blog2", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("blog2.html", {"request": request, "message": "success"})


@router.post("/admin/create-blog")
async def create_blog_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None
    if file:
        image_data = await file.read()
        image_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(image_path, "wb") as f:
            f.write(image_data)
        image_url = f"template/blog/images{file.filename}"

    try:
        blog = CreateBlog(title=title, content=content)
        new_blog = create_new_blog(blog=blog, db=db, author_id=1, image_url=image_url)
        return RedirectResponse(url="/admin?message=Blog created successfully", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/delete-blog/{blog_id}")
async def delete_blog_post(request: Request, blog_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    current_user_id = current_user.id  
    try:
        result = delete_blog_by_id(id=blog_id, db=db, author_id=current_user_id)
        if "error" in result:
            return RedirectResponse(url=f"/admin?message={result['error']}", status_code=303)
        return RedirectResponse(url="/admin?message=Blog deleted successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin?message=Error deleting blog: {str(e)}", status_code=303)