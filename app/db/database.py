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

SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
