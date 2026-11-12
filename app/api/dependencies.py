from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.product import ProductService
from app.database.session import get_session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]

def get_product_service_session(session: SessionDependency):
    return ProductService(session)

ServiceDependency = Annotated[ProductService, Depends(get_product_service_session)]