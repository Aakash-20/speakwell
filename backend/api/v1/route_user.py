from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, ShowUser
from db.session import get_db
from db.repository.user import create_new_user
import logging

router = APIRouter()

@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await create_new_user(user=user, db=db)
        
        logging.info(f"Created user: {new_user.__dict__}")
        
        show_user = ShowUser(
            id=new_user.id,
            email=new_user.email,
            is_active=new_user.is_active
        )
        
        return show_user
    except Exception as e:
        logging.error(f"Error creating user: {repr(e)}")
        await db.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )