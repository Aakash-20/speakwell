from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Set up Jinja2Templates
templates = Jinja2Templates(directory="/home/harsh/speakwell/speakwell/backend/template1")

@router.get("/keyfactor")
async def get_keyfactor(request: Request):
    # Render the template
    return templates.TemplateResponse("keyfactor.html", {"request": request})