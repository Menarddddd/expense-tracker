from fastapi import FastAPI
from contextlib import asynccontextmanager

from user_route import router as user_router
from database import engine, Base


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api/users", tags=["users"])
