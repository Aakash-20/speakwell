from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from random import randint
import uuid
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.image import Image
from schemas.image import  ImageResponse, ImageUploadResponse

IMAGEDIR = "images/"

router = APIRouter()


def get_base_url(request: Request):
    return f"{request.base_url}"


@router.post("/upload", response_model=ImageUploadResponse)
async def create_upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    request: Request = Depends()
):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    base_url = get_base_url(request)
    url = f"{base_url}images/{file.filename}"

    db_image = Image(filename=file.filename, url=url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return {"filename": file.filename, "url": url}

@router.get("/show", response_model=ImageResponse)
async def read_random_file(db: Session = Depends(get_db), request: Request):
    images = db.query(Image).all()
    
    if not images:
        raise HTTPException(status_code=404, detail="No images found")

    random_image = images[randint(0, len(images) - 1)]
    
    base_url = get_base_url(request)
    url = f"{base_url}images/{random_image.filename}"
    
    return ImageResponse(
        id=random_image.id,
        filename=random_image.filename,
        url=url,
        created_at=random_image.created_at
    )
