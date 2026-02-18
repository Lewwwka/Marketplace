from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.auth.router import router as auth_router
from app.api.users.router import router as users_router
from app.api.orders.router import router as orders_router
from app.api.products.router import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(product_router)
