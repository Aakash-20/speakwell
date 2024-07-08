from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, list_blogs, update_blog_by_id

router = APIRouter()

@router.post("/", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    try:
        blog = create_new_blog(blog=blog, db=db, author_id= 1)
        return blog
    except Exception as e:
            print(repr(e))


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
def update_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db)):
    try:
        blog = update_blog_by_id(id=id, blog=blog,db=db, author_id=1)
        if not blog:
            raise HTTPException(detail=f"Blog with {id} does not exists")
        return blog
    except Exception as e:
            print(repr(e))