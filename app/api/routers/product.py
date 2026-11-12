from fastapi import APIRouter

from fastapi import HTTPException, status
from fastapi.concurrency import asynccontextmanager
from app.database.session import ServiceDependency
from app.schema.models import CreateProduct, ReadProduct, UpdateProduct
from app.database.models import Product


router = APIRouter()

@router.get("/product/{id}", response_model = ReadProduct)
async def get_product_by_id(id:int, service: ServiceDependency):
    product = await service.get(id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with given ID doesn't exist")
    return product

@router.post("/product", response_model= ReadProduct)
async def create_product(data: CreateProduct, service: ServiceDependency):
    return await service.add(data)

@router.put("/product", response_model=ReadProduct)
async def  update_product(id:int, data:UpdateProduct, service: ServiceDependency):    
    updated_data = data.model_dump(exclude_none=True)
    if updated_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "No updated data provided")
    product = await service.update(id, updated_data)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with given ID doesn't exist")
    return product

@router.delete("/product")
async def delete_product(id:int, service: ServiceDependency) -> dict[str, str]:
    if not await service.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with given ID doesn't exist")
    return {"detail":f"Deleted product with {id}"}
