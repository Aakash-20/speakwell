from db.models.image import Image
from schemas.image import ImageListResponse
from typing import List
from fastapi import Request
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.image import Image


IMAGEDIR = "template/gallery"


async def get_all_images_logic(request: Request, db: AsyncSession) -> List[ImageListResponse]:
    query = select(Image).order_by(desc(Image.created_at)).limit(10)
    result = await db.execute(query)
    db_images = result.scalars().all()

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