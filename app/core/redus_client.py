import redis.asyncio as redis

from ..core.config import settings


redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    assert redis_client is not None
    return redis_client


async def init_redis() -> None:
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis.from_url(
            url=settings.REDIS_URL,
            decode_responses=True,
        )


async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None
