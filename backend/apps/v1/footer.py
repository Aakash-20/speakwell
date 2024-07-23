from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/footer", response_class=HTMLResponse)
async def get_footer(request : Request):
    file_path = os.path.join(os.path.dirname(__file__), 'backend\template1\footer.html')
    file_path = os.path.abspath(file_path)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path) as f:
        return f.read()