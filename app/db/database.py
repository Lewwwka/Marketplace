from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


sync_engine = create_engine(
    url=settings.DATABASE_URL,
    echo=True,
)

async_engine = create_async_engine(
    url=settings.DATABASE_ASYNC_URL,
    echo=True,
)

SessionLocal = sessionmaker(sync_engine)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
