from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Product
from app.schema.models import CreateProduct, UpdateProduct

class ProductService:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get(self, id:int) -> Product | None:
        return await self.session.get(Product, id)
    
    async def add(self, data: CreateProduct) -> Product:
        new_product = Product(**data.model_dump())
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product
    
    async def update(self, id: int, data: dict) -> Product | None:
        product = await self.session.get(Product, id)
        if product is None:
            return None
        product.sqlmodel_update(data)
        await self.session.commit()
        await self.session.refresh(product)
        return product
    
    async def delete(self, id:int) -> bool:
        product = await self.session.get(Product, id)
        if product is None:
            return False
        await self.session.delete(product)
        await self.session.commit()
        return True
    