from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Set up Jinja2Templates
templates = Jinja2Templates(directory="template1")

@router.get("/header")
async def get_header(request: Request):
    return templates.TemplateResponse("header.html", {"request": request})