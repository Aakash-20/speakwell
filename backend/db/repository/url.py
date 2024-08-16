from sqlalchemy.orm import Session
from db.models.url import URL
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_url_by_id(db: AsyncSession, url_id: int):
    result = await db.execute(select(URL).filter(URL.id == url_id))
    return result.scalar_one_or_none()

def update_url(db: Session, url_id: int, new_url: str):
    url_obj = get_url_by_id(db, url_id)
    if url_obj:
        url_obj.url = new_url
        db.commit()
        db.refresh(url_obj)
    return url_obj