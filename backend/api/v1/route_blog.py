from fastapi import APIRouter, status, Depends, HTTPException, Form, UploadFile, File
from typing import List, Optional
import os
from fastapi import Request
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.user import User
from db.models.blog import Blog
from api.v1.route_login import get_current_user
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, list_blogs, update_blog_by_id, delete_blog_by_id
from core.config import settings

UPLOAD_DIR = "upload"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


router = APIRouter()

def save_image_to_db(db, filename, file_path):
    image = Blog.image(filename=filename, file_path=file_path)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.post("/", response_model=ShowBlog, status_code=201)
async def create_blog(request: Request, blog: CreateBlog = Depends(CreateBlog), file: UploadFile = File(None), db: Session = Depends(get_db)):
    image_url = None
    if file:
        image_data = file.file.read()
        image_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        image_url = f"{request.base_url}images/{file.filename}"

    try:
        blog = create_new_blog(blog=blog, db=db, author_id=1, image_url=image_url)
        return blog
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    try:
        blog = retrieve_blog(id=id, db=db)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
        return blog
    except Exception as e:
            print(repr(e))


@router.get("", response_model=List[ShowBlog])
def get_all_active_blogs(db: Session = Depends(get_db)):
    try:
        blogs = list_blogs(db=db)
        return blogs
    except Exception as e:
            print(repr(e))


@router.put("/{id}", response_model=ShowBlog)
def update_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        blog = update_blog_by_id(id=id, blog=blog,db=db, author_id=current_user.id)
        if isinstance(blog, dict):
             raise HTTPException(
                  detail= blog.get("error"),
                  status_code=status.HTTP_400_BAD_REQUEST
             )
        if not blog:
            raise HTTPException(detail=f"Blog with {id} does not exists")
        return blog
    except Exception as e:
            print(repr(e))


@router.delete("/{id}")
def delete_a_blog(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
     message = delete_blog_by_id(id = id, db=db, author_id= current_user.id)
     if message.get("error"):
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message.get("error"))
     return {"message": message.get("msg")}