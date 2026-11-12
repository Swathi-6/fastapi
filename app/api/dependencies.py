from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.product import ProductService
from app.database.session import get_session
from app.services.seller import SellerService
from app.utils import decode_access_token
from app.core.security import oauth2_scheme
from app.database.models import Seller
from app.database.redis import is_jwti_blacklisted


SessionDependency = Annotated[AsyncSession, Depends(get_session)]

def get_product_service_session(session: SessionDependency):
    return ProductService(session)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service_session)]


def get_seller_service_session(session: SessionDependency):
    return SellerService(session)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service_session)]

# Access token data
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = decode_access_token(token)
    # if data is None or await is_jwti_blacklisted(data["jwti"]):
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    return data

# get logged in user
async def get_current_seller(token_data: Annotated[dict, Depends(get_access_token)], session: SessionDependency):
    return await session.get(Seller, token_data["user"]["id"])

SellerDep = Annotated[Seller, Depends(get_current_seller)]


