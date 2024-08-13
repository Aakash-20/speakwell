from sqlalchemy.orm import Session
from db.models.url import URL


def get_url_by_id(db: Session, url_id: int):
    return db.query(URL).filter(URL.id == url_id).first()


def update_url(db: Session, url_id: int, new_url: str):
    url_obj = get_url_by_id(db, url_id)
    if url_obj:
        url_obj.url = new_url
        db.commit()
        db.refresh(url_obj)
    return url_obj