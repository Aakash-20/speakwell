from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory="template1")

@router.get("/footer")
async def get_footer(request: Request):
    return templates.TemplateResponse("footer.html", {"request": request})