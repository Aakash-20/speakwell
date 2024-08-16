from fastapi import APIRouter, Depends, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from schemas.address import AddressCreate
from db.repository.address import create_new_address, remove_address

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/address")
async def create_address(address: str = Form(...), db: AsyncSession = Depends(get_db)):
    address_create = AddressCreate(address=address)
    await create_new_address(address_create, db)
    return RedirectResponse(url="/admin_contact", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/remove_address/{address_id}")
async def delete_address(address_id: int, db: AsyncSession = Depends(get_db)):
    await remove_address(address_id, db)
    return RedirectResponse(url="/admin_contact", status_code=status.HTTP_303_SEE_OTHER)