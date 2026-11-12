from fastapi import APIRouter

from fastapi import HTTPException, status
from app.api.schema.product import CreateProduct, ReadProduct, UpdateProduct
from app.database.models import Product
from app.api.dependencies import ProductDep


router = APIRouter(prefix="/product/v1", tags=["Product"])

@router.get("/", response_model = ReadProduct)
async def get_product_by_id(id:int, service: ProductDep):
    product = await service.get(id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with given ID doesn't exist")
    return product

@router.post("/", response_model= ReadProduct)
async def create_product(data: CreateProduct, service: ProductDep):
    return await service.add(data)

@router.put("/", response_model=ReadProduct)
async def  update_product(id:int, data:UpdateProduct, service: ProductDep):    
    updated_data = data.model_dump(exclude_none=True)
    if updated_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "No updated data provided")
    product = await service.update(id, updated_data)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with given ID doesn't exist")
    return product

@router.delete("/")
async def delete_product(id:int, service: ProductDep) -> dict[str, str]:
    if not await service.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with given ID doesn't exist")
    return {"detail":f"Deleted product with {id}"}
