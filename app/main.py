from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.auth.router import router as auth_router
from app.api.users.router import router as users_router
from app.api.orders.router import router as orders_router
from app.api.products.router import router as product_router
from app.core.middleware import ErrorHandlingMiddleware, TimingMiddleware
from app.core.redus_client import init_redis, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    yield
    await close_redis()


app = FastAPI(lifespan=lifespan)

app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(TimingMiddleware)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(product_router)
