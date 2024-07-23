from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory="template1")

@router.get("/why_us")
async def get_why_us(request: Request):
    return templates.TemplateResponse("whyUs.html", {"request": request})