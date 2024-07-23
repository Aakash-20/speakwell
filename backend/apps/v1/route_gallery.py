from fastapi import Request, Form, Query, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="template1")
router = APIRouter()

@router.get("/gallery", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request, "message": "success"})
