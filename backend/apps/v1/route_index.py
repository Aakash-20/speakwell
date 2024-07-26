from fastapi import Request, Form, Query, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="template")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("admin_index.html", {"request": request, "message": "success"})

@router.get("/aboutUs", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("aboutUs.html", {"request": request, "message": "success"})

@router.get("/footer")
async def get_footer(request: Request):
    return templates.TemplateResponse("footer.html", {"request": request})

@router.get("/keyfactor")
async def get_keyfactor(request: Request):
    return templates.TemplateResponse("keyfactor.html", {"request": request})

@router.get("/header")
async def get_header(request: Request):
    return templates.TemplateResponse("header.html", {"request": request})

@router.get("/whatsapp", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("whatsapp.html", {"request": request, "message": "success"})

@router.get("/gallery", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request, "message": "success"})

@router.get("/why_us")
async def get_why_us(request: Request):
    return templates.TemplateResponse("whyUs.html", {"request": request})


