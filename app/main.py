from typing import Any

from fastapi import FastAPI, APIRouter
from fastapi.concurrency import asynccontextmanager
from app.database.session import create_db_tables
from app.api.routers import product

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(product.router)