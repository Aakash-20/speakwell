from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
import asyncio

async def create_engine_with_retry(max_retries=3, retry_interval=5):
    for attempt in range(max_retries):
        try:
            engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
            async with engine.connect() as conn:
                await conn.execute("SELECT 1")
            return engine
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
            await asyncio.sleep(retry_interval)

# Create a global variable for the engine
engine = None

# Create a function to get or create the engine
async def get_engine():
    global engine
    if engine is None:
        engine = await create_engine_with_retry()
    return engine

# Modify the get_db function to use the async engine
async def get_db():
    engine = await get_engine()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()