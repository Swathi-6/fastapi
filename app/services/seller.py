from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schema.seller import CreateSeller, ReadSeller
from app.database.models import Seller
from app.config import security_settings

from passlib.context import CryptContext
from app.utils import generate_access_token, decode_access_token

pwd_context = CryptContext(schemes="bcrypt")

class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add(self, credentials: CreateSeller) -> Seller:
        seller = Seller(**credentials.model_dump(exclude={"password"}), hash_password=pwd_context.hash(credentials.password))
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
    
    async def login(self, email, password) -> str:
        # Validating user login details
        result = await self.session.execute(select(Seller).where(Seller.email == email))
        seller = result.scalar()
        if seller is None or not pwd_context.verify(password, seller.hash_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Generating jwt token
        token = generate_access_token(
            {
                "user":{
                    "id":seller.id
                } 
            }
        )
        return token

    