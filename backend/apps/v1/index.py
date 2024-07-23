from fastapi.responses import HTMLResponse
from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/index.html", response_class=HTMLResponse)
async def get_index():
    # Get the absolute path to the header.html file
    file_path = os.path.join(os.path.dirname(__file__), '/home/harsh/speakwell/speakwell/backend/template1/index.html')
    file_path = os.path.abspath(file_path)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path) as f:
        return f.read()