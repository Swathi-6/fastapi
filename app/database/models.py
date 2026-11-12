from datetime import datetime, timezone
from enum import Enum

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    ACCESSORIES = "accessories"


class Product(SQLModel, table=True):
    __tablename__ = "product"  # type: ignore
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=30)
    price: int = Field(gt=0)
    stock: int = Field(ge=0)
    category: ProductCategory
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
class Seller(SQLModel, table=True):
    __tablename__ = "seller"     #type: ignore
    id: int = Field(default=None, primary_key=True)
    name: str 
    email: EmailStr
    hash_password: str
    