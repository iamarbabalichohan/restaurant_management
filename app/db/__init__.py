from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

async_engine = create_async_engine(settings.database_url)

ASYNC_LOCAL_SESSION = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    ...
    
async def get_async_db():
    try:
        async with ASYNC_LOCAL_SESSION() as db:
            yield db
    finally:
        db.close()