import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from db.models.image import Image
from schemas.image import ImageResponse
from typing import List


IMAGEDIR = "template/gallery"


def get_base_url(request):
    return f"{request.base_url}"


async def create_upload_files_logic(request, files: List[UploadFile], db: Session):
    os.makedirs(IMAGEDIR, exist_ok=True)
    
    uploaded_files = []
    for file in files:
        filename = file.filename
        contents = await file.read()

        file_path = os.path.join(IMAGEDIR, filename)
        with open(file_path, "wb") as f:
            f.write(contents)

        base_url = get_base_url(request)
        url = f"{base_url}images/{filename}"

        db_image = Image(filename=filename, url=url)
        db.add(db_image)
        
        uploaded_files.append({"filename": filename, "url": url})
    
    db.commit()
    return uploaded_files


async def create_upload_file_logic(request, file, db: Session):
    filename = file.filename
    contents = await file.read()

    os.makedirs(IMAGEDIR, exist_ok=True)

    file_path = os.path.join(IMAGEDIR, filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    base_url = get_base_url(request)
    url = f"{base_url}images/{filename}"

    db_image = Image(filename=filename, url=url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return {"filename": filename, "url": url}


async def get_image_info_logic(filename: str, request, db: Session):
    db_image = db.query(Image).filter(Image.filename == filename).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    base_url = get_base_url(request)
    url = f"{base_url}image/get/{filename}"

    return ImageResponse(
        id=db_image.id,
        filename=db_image.filename,
        url=url,
        created_at=db_image.created_at
    )