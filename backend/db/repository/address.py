from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from schemas.address import AddressCreate
from db.models.address import Address

async def create_new_address(address: AddressCreate, db: AsyncSession):
    new_address = Address(address=address.address)
    db.add(new_address)
    await db.commit()
    await db.refresh(new_address)
    return new_address

async def list_addresses(db: AsyncSession) -> List[Address]:
    result = await db.execute(select(Address).order_by(desc(Address.created_at)))
    return result.scalars().all()

async def remove_address(address_id: int, db: AsyncSession):
    result = await db.execute(select(Address).filter(Address.id == address_id))
    address = result.scalar_one_or_none()
    if address:
        await db.delete(address)
        await db.commit()
    return None