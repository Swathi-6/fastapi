from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schema.seller import CreateSeller, ReadSeller
from app.api.dependencies import SellerDep
from app.database.models import Seller
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/login")

router = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/signup", response_model=ReadSeller)
async def register_seller(seller: CreateSeller, service: SellerDep):
    return await service.add(seller)

@router.post("/login")
async def login(service: SellerDep, request_form: OAuth2PasswordRequestForm = Depends()):
    token = await service.login(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }