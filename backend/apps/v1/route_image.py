from fastapi import APIRouter, Request, Depends, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from sqlalchemy.exc import IntegrityError
from db.repository.image import create_upload_file_logic
from db.models.image import Image
import os


router = APIRouter()
templates = Jinja2Templates(directory="template")

IMAGEDIR = "template/gallery"


@router.post("/upload", response_class=HTMLResponse)
async def create_upload_file(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        result = await create_upload_file_logic(request, file, db)
        return templates.TemplateResponse(
            "admin_image.html",
            {"request": request, "success_message": "File uploaded successfully", "file_info": result}
        )
    except IntegrityError:
        db.rollback()  
        return templates.TemplateResponse(
            "admin_image.html",
            {"request": request, "error_message": "An image with this name already exists"}
        )
    except Exception as e:
        print(repr(e))
        return templates.TemplateResponse(
            "admin_image.html",
            {"request": request, "error_message": "An error occurred while uploading your file"}
        )
    


@router.post("/admin_image/delete/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        db.delete(image)
        db.commit()
        os.remove(f"template/gallery/{image.filename}")
        return RedirectResponse(url="/admin_image", status_code=303)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

