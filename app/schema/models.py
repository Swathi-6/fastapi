from enum import Enum
import random

from pydantic import BaseModel, Field

def generate_warehouse()->int:
    return random.randint(1,5)

class ProductStatus(str, Enum):
    active = "active"
    low = "low stock"
    out = "out of stock"
    

class BaseProduct(BaseModel):
    name: str = Field(min_length=3, max_length=20, description="Product title")
    price: float = Field(gt=0, lt=1000, description="Product price")
    stock: int = Field(gt=0, lt=100, description="Available in stock")
    warehouse: int = Field(default_factory=generate_warehouse, description="Warehouse Number (1-5)")

class CreateProduct(BaseProduct):
    pass

class ReadProduct(BaseProduct):
    pass
    
class UpdateProduct(BaseProduct):
    name: str | None = Field(default=None, min_length=3, max_length=20, description="Product title")
    price: float | None = Field(default=None, gt=0, lt=1000, description="Product price")
    stock: int | None= Field(default=None, gt=0, lt=100, description="Available in stock")
    warehouse: int | None = Field(default=None, description="Warehouse Number (1-5)")
    