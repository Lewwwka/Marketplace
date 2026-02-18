from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)
