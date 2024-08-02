from typing import Optional, List, Dict, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc
from schemas.blog import CreateBlog, UpdateBlog
from db.models.blog import Blog


def create_new_blog(blog: CreateBlog, db: Session, author_id: int, image_url: Optional[str] = None) -> Blog:
    new_blog = Blog(
        title=blog.title,
        content=blog.content,
        slug=blog.slug,
        author_id=author_id,
        image=image_url
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def retrieve_blog(id: int, db: Session) -> Optional[Blog]:
    try:
        return db.query(Blog).filter(Blog.id == id).first()
    except Exception as e:
        print(f"Error retrieving blog: {repr(e)}")
        return None


def list_blogs(db: Session) -> List[Blog]:
    return db.query(Blog).order_by(desc(Blog.created_at)).all()


def update_blog_by_id(id: int, blog: UpdateBlog, db: Session, author_id: int) -> Union[Blog, Dict[str, str]]:
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error": f"Blog with id {id} does not exist"}
    if blog_in_db.author_id != author_id:
        return {"error": "Only the author can modify the blog"}

    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    db.add(blog_in_db)
    db.commit()
    db.refresh(blog_in_db)
    return blog_in_db


def delete_blog_by_id(id: int, db: Session, author_id: int) -> Dict[str, str]:
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error": f"Could not find blog with the id {id}"}
    if blog_in_db.author_id != author_id:
        return {"error": "Only the author can delete the blog"}
    
    db.delete(blog_in_db)
    db.commit()
    return {"msg": f"Deleted blog with id {id}"}