from fastapi import APIRouter, Request, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from sqlalchemy.exc import IntegrityError
from db.repository.image import is_admin
from db.models.image import Image
from fastapi.security.utils import get_authorization_scheme_param
from api.v1.route_login import get_current_user
import os


router = APIRouter()
templates = Jinja2Templates(directory="template")


IMAGEDIR = "template/gallery"


@router.post("/upload", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        current_user = get_current_user(token=token, db=db)
        if not is_admin(current_user.id):
            return RedirectResponse(
                url="/admin_index?message=You do not have permission to upload image",
                status_code=status.HTTP_303_SEE_OTHER)
        
        # Create the directory if it doesn't exist
        os.makedirs(IMAGEDIR, exist_ok=True)
        
        file_path = os.path.join(IMAGEDIR, file.filename)
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Generate the URL for the image using the base URL
        image_url = f"{request.base_url}image_gallery/{file.filename}"
        
        # Save image information to database (assuming you have an Image model)
        new_image = Image(filename=file.filename, url=image_url)
        db.add(new_image)
        db.commit()
        
        return RedirectResponse(url="/admin_image?message=Image uploaded successfully", status_code=status.HTTP_303_SEE_OTHER)
    except IntegrityError:
        db.rollback()  
        return RedirectResponse(url="/admin_image?message=An image with this name already exists", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return RedirectResponse(url="/admin_image?message=An error occurred while uploading your file", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/admin_image/delete/{image_id}")
def delete_image(request: Request, image_id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        current_user = get_current_user(token=token, db=db)
        if not is_admin(current_user.id):
            return RedirectResponse(
                url="/admin_index?message=You do not have permission to delete image",
                status_code=status.HTTP_303_SEE_OTHER)
        
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        file_path = os.path.join(IMAGEDIR, image.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.delete(image)
        db.commit()
        
        alert = "Image deleted successfully"
        return RedirectResponse(
            f"/admin_image?alert={alert}", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException as he:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "alert": he.detail, "image_id": image_id}
        )
    except Exception as e:
        print(f"Exception raised while deleting image: {e}")
        db.rollback()
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "alert": "An error occurred", "image_id": image_id}
        )