import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.db.database import get_db
from app.db.models import Base
from app.core.config import settings
from app.api.dependencies import get_redis_client


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db_once():

    engine = create_async_engine(settings.DATABASE_ASYNC_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client():

    async def override_get_db():
        engine = create_async_engine(settings.DATABASE_ASYNC_URL)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        async with async_session() as session:
            try:
                yield session
                await session.commit()
            except:
                await session.rollback()
                raise
            finally:
                await session.close()

        await engine.dispose()

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def logged_in_token(client: AsyncClient):

    login_data = {
        "email": "user@example.com",
        "password": "stringst",
    }

    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 200

    return response.json()["access_token"]


@pytest_asyncio.fixture
async def auth_client(logged_in_token: str):

    class RedisMock:
        def pipeline(self):

            class Pipe:
                def hset(self, *args):
                    return self

                def expire(self, *args):
                    return self

                async def execute(self):
                    return [True, True, True]

            return Pipe()

        async def hgetall(self, key):
            return {b"1": b"2"}

        async def delete(self, key):
            return 1

    app.dependency_overrides[get_redis_client] = lambda: RedisMock()

    headers = {"Authorization": f"Bearer {logged_in_token}"}

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers=headers,
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
