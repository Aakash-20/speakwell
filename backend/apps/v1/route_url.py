from fastapi import APIRouter, Depends, Form, status, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from db.session import get_db
from db.repository.url import update_url


router = APIRouter()


@router.post("/admin/url/1")
async def update_url_route(request: Request, url: str = Form(...), db: Session = Depends(get_db)):
    url_obj = update_url(db, url_id=1, new_url=url)
    return RedirectResponse(url="/admin_review", status_code=status.HTTP_303_SEE_OTHER)
