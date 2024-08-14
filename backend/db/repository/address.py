from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from schemas.address import AddressCreate
from db.models.address import Address


def create_new_address(address: AddressCreate, db: Session):
    new_address = Address(
        address=address.address  
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


def list_addresses(db: Session) -> List[Address]:
    return db.query(Address).order_by(desc(Address.created_at)).all()


def remove_address(address_id: int, db: Session):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address:
        db.delete(address)
        db.commit()
    return None