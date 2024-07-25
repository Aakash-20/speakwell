from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="template")
router = APIRouter()

@router.get("/admin", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("admin_index.html", {"request": request, "message": "success"})


@router.get("/admin_enquiry", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("admin_enquiry.html", {"request": request, "message": "success"})


@router.get("/admin_contactus", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("admin_contact.html", {"request": request, "message": "success"})


@router.get("/admin_image", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("admin_image.html", {"request": request, "message": "success"})
