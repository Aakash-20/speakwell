from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import desc
from schemas.blog import CreateBlog
import os
from db.models.blog import Blog
from urllib.parse import urlparse


UPLOAD_DIR = "template/blog/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    return db.query(Blog).order_by(desc(Blog.created_at)).limit(10).all()


def delete_blog_by_id(id: int, db: Session, author_id: int) -> Dict[str, str]:
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error": f"Could not find blog with the id {id}"}
    if blog_in_db.author_id != author_id:
        return {"error": "Only the author can delete the blog"}
    
    # Extract the filename from the image URL
    if blog_in_db.image:
        # Parse the URL to extract the path
        parsed_url = urlparse(blog_in_db.image)
        # Extract the filename
        filename = os.path.basename(parsed_url.path)
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Delete the image file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.delete(blog_in_db)
    db.commit()
    return {"msg": f"Deleted blog with id {id}"}



def save_image_to_db(db, filename, file_path):
    image = Blog.image(filename=filename, file_path=file_path)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def is_admin(user_id: int) -> bool:
    return user_id == 1