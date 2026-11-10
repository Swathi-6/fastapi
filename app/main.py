from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from schema.models import BaseProduct, CreateProduct, ReadProduct, UpdateProduct, ProductStatus
from database import Database

app = FastAPI()
db = Database()

@app.get("/product")
def get_products():
    return db.get_all()


@app.get("/product/{id}")
def get_product_by_id(id:int)-> dict[str, Any] | None:
    product = db.get(id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    return product


@app.post("/product")
def create_product(data: CreateProduct) -> dict[str, Any]:
    new_id = db.create(data)
    return {'id':new_id}


@app.put("/product")
def  update_product(id:int, data:UpdateProduct)-> dict[str, Any]:
    updated_data = db.update(id, data)
    if updated_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    return updated_data


@app.delete("/product")
def delete_product(id:int):
    db.delete(id)
    return {"detail":f"Deleted product with {id}"}

