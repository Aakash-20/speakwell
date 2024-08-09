from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from typing import List, Dict
import os
from fastapi import Request
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.blog import Blog
from api.v1.route_login import get_current_user
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, list_blogs, update_blog_by_id, delete_blog_by_id, save_image_to_db, is_admin


UPLOAD_DIR = "template/blog/images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


router = APIRouter()


@router.get("/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    try:
        blog = retrieve_blog(id=id, db=db)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
        return blog
    except HTTPException as e:
        raise e  
    except Exception as e:
        print(f"Unexpected error: {repr(e)}")  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@router.get("/", response_model=List[ShowBlog])
def get_all_active_blogs(db: Session = Depends(get_db)):
    try:
        blogs = list_blogs(db=db)
        return blogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ShowBlog, status_code=201)
async def create_blog(request: Request, blog: CreateBlog = Depends(CreateBlog), 
                      file: UploadFile = File(None), db: Session = Depends(get_db),
                      current_user = Depends(get_current_user)):
    if not is_admin(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Only admin can create blog posts")
    image_url = None
    if file:
        image_data = file.file.read()
        image_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(image_path, "wb") as f:
            f.write(image_data)
        image_url = f"{request.base_url}images/{file.filename}"
    try:
        blog = create_new_blog(blog=blog, db=db, author_id=current_user.id, image_url=image_url)
        print(f"Created blog: {blog.__dict__}")  
        return blog
    except Exception as e:
        print(f"Error creating blog: {str(e)}")  
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}", response_model=ShowBlog)
def update_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not is_admin(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Only admin can update blog posts")
    existing_blog = retrieve_blog(id=id, db=db)
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id {id} does not exist")
    try:
        updated_blog = update_blog_by_id(id=id, blog=blog, db=db, author_id=current_user.id)
        if isinstance(updated_blog, dict) and "error" in updated_blog:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=updated_blog["error"])
        return updated_blog
    except Exception as e:
        print(f"Unexpected error: {repr(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="An unexpected error occurred")


@router.delete("/{id}", response_model=Dict[str, str])
def delete_a_blog(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not is_admin(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can delete blog posts")
    existing_blog = retrieve_blog(id=id, db=db)
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    if existing_blog.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the author can delete the blog")
    try:
        message = delete_blog_by_id(id=id, db=db, author_id=current_user.id)
        if "error" in message:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message["error"])
        return {"message": message["msg"]}
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))