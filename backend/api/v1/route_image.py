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


# @app.post("/upload")
# async def upload_image(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
#     image_data = file.file.read()
#     image_path = os.path.join(UPLOAD_DIR, file.filename)

#     with open(image_path, "wb") as f:
#         f.write(image_data)

#     try:
#         image_obj = save_image_to_db(db, file.filename, image_path)
#         base_url = request.base_url
#         image_url = f"{base_url}images/{file.filename}"
#         return {"status": 200, "message": "Image uploaded successfully",
#                 "data": {"image_id": image_obj.id, "image_url": image_url}}
#     finally:
#         db.close()


# @app.get("/images/{filename}")
# async def get_image(filename: str):
#     image_path = os.path.join(UPLOAD_DIR, filename)
#     if not os.path.exists(image_path):
#         logging.error(f"Image not found: {filename}")
#         raise HTTPException(status_code=404, detail="Image not found")
#     return FileResponse(image_path)


# @app.post("/multipleUpload")
# async def upload_image(request: Request, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
#     image_urls = []
#     for file in files:
#         contents = await file.read()
#         filename = file.filename
#         file_path = os.path.join(UPLOAD_DIR, filename)

#         with open(file_path, "wb") as f:
#             f.write(contents)

#         image = Image(filename=filename, file_path=file_path)
#         try:
#             db.add(image)
#             db.commit()
#             db.refresh(image)
#         except Exception as e:
#             logging.error(f"Error storing image {filename}: {e}")
#             db.rollback()
#         finally:
#             db.close()
#         base_url = request.base_url
#         image_url = f"{base_url}images/{file.filename}"
#         image_urls.append(image_url)

#     return {"status": 200, "message": "Images uploaded successfully", "data": {"image_url": image_urls}}