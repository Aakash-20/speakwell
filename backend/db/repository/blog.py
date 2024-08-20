from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from schemas.blog import CreateBlog
import os
from db.models.blog import Blog
from urllib.parse import urlparse
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession



UPLOAD_DIR = "template/blog/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def create_new_blog(blog: CreateBlog, db: Session, author_id: int, image_url: Optional[str] = None) -> Blog:
    new_blog = Blog(
        title=blog.title,
        content=blog.content,
        slug=blog.slug,
        author_id=author_id,
        image=image_url
    )
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

async def retrieve_blog(id: int, db: AsyncSession) -> Optional[Blog]:
    result = await db.execute(select(Blog).filter(Blog.id == id))
    return result.scalar_one_or_none()

async def list_blogs(db: AsyncSession) -> List[Blog]:
    result = await db.execute(select(Blog).order_by(desc(Blog.created_at)).limit(10))
    return result.scalars().all()

async def delete_blog_by_id(id: int, db: AsyncSession, author_id: int) -> Dict[str, str]:
    result = await db.execute(select(Blog).filter(Blog.id == id))
    blog_in_db = result.scalar_one_or_none()
    if not blog_in_db:
        raise HTTPException(status_code=404, detail=f"Could not find blog with the id {id}")
    if blog_in_db.author_id != author_id:
        raise HTTPException(status_code=403, detail="Only the author can delete the blog")
    
    if blog_in_db.image:
        parsed_url = urlparse(blog_in_db.image)
        filename = os.path.basename(parsed_url.path)
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    await db.delete(blog_in_db)
    await db.commit()
    return {"msg": f"Deleted blog with id {id}"}