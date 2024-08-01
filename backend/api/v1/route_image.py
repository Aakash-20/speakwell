from fastapi import APIRouter, File, UploadFile, Depends, Request
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.image import ImageResponse, ImageUploadResponse
from db.repository.image import create_upload_file_logic, get_image_info_logic, create_upload_files_logic
from typing import List


router = APIRouter()


@router.post("/upload-multiple", response_model=List[ImageUploadResponse])
async def create_upload_files(
    request: Request,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    return await create_upload_files_logic(request, files, db)


@router.post("/upload", response_model=ImageUploadResponse)
async def create_upload_file(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await create_upload_file_logic(request, file, db)


@router.get("/info", response_model=ImageResponse)
async def get_image_info(filename: str, request: Request, db: Session = Depends(get_db)):
    return await get_image_info_logic(filename, request, db)