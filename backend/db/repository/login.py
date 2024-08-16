from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.user import User

async def get_user_by_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    return user