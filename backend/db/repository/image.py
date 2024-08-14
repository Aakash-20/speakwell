from sqlalchemy.orm import Session
from db.models.image import Image
from sqlalchemy import desc
from schemas.image import ImageListResponse
from typing import List
from fastapi import Request


IMAGEDIR = "template/gallery"


async def get_all_images_logic(request: Request, db: Session) -> List[ImageListResponse]:
    db_images = db.query(Image).order_by(desc(Image.created_at)).limit(10).all()
    if not db_images:
        return [] 
    base_url = str(request.base_url)
    image_list = []
    for db_image in db_images:
        url = f"{base_url}image_gallery/{db_image.filename}"
        image_response = ImageListResponse(
            id=db_image.id,
            filename=db_image.filename,
            url=url,
            created_at=db_image.created_at
        )
        image_list.append(image_response)
    return image_list


def get_all_images(db: Session) -> List[dict]:
    db_images = db.query(Image).order_by(desc(Image.created_at)).all()
    return [
        {
            "id": image.id,
            "filename": image.filename,
            "image_url": image.url
        }
        for image in db_images
    ]


