from sqlalchemy.orm import Session
from schemas.blog import CreateBlog, UpdateBlog
from db.models.blog import Blog

def create_new_blog(blog: CreateBlog, db : Session, author_id : int = 1):
    blog = Blog(title = blog.title,
                slug=blog.slug,
                content=blog.content,
                author_id=author_id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog
    
def retrieve_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog

def list_blogs(db:Session):
    blogs = db.query(Blog).filter(Blog.is_active == True).all()
    return blogs

def update_blog_by_id(id: int, blog: UpdateBlog, db: Session, author_id: int = 1):
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return
    blog_in_db.title = blog.title
    blog_in_db.slug = blog.slug
    blog_in_db.content = blog.content
    db.add(blog_in_db)
    db.commit()
    return blog_in_db
    
