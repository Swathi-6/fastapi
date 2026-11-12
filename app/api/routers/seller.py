from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from redis import RedisError

from app.api.schema.seller import CreateSeller, ReadSeller
from app.api.dependencies import SellerServiceDep, get_access_token
from app.database.models import Seller
from app.database.redis import add_jwti_to_blacklist


router = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/signup", response_model=ReadSeller)
async def register_seller(seller: CreateSeller, service: SellerServiceDep):
    return await service.add(seller)

@router.post("/login")
async def login(service: SellerServiceDep, request_form: OAuth2PasswordRequestForm = Depends()):
    token = await service.login(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }
    
@router.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_access_token)]):
    # await add_jwti_to_blacklist(token_data["jwti"])
    return {"detail": "Logged out!"}