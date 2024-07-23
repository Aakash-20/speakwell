from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="template1")
router = APIRouter()

@router.get("/aboutUs", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("aboutUs.html", {"request": request, "message": "success"})
