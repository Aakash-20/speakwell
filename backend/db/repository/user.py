from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
from db.models.user import User
from core.hashing import Hasher

async def create_new_user(user: UserCreate, db: AsyncSession):
    new_user = User(
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user