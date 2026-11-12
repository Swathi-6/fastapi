from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, Session
from app.config import settings
from app.services.product import ProductService

# create db engine asynchronously
engine = create_async_engine(settings.POSTGRES_URL, echo=True)

# create session factory async
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# create tables
async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
# dependency
async def get_session():
    async with async_session() as session:
        yield session
        
SessionDependency = Annotated[AsyncSession, Depends(get_session)]

def get_product_service_session(session: SessionDependency):
    return ProductService(session)

ServiceDependency = Annotated[ProductService, Depends(get_product_service_session)]
