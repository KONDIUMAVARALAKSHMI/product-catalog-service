from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from src.schemas.product import Product, ProductCreate, ProductUpdate
from src.services.product_service import ProductService
from src.unit_of_work.sql_uow import SqlUnitOfWork
from src.database import SessionLocal

router = APIRouter()

def get_product_service():
    uow = SqlUnitOfWork(SessionLocal)
    return ProductService(uow)

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, service: ProductService = Depends(get_product_service)):
    return service.create_product(product_in.dict(exclude={"category_ids"}), [str(cid) for cid in product_in.category_ids])

@router.get("/search", response_model=List[Product])
def search_products(
    q: Optional[str] = None,
    category_id: Optional[UUID] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 10,
    service: ProductService = Depends(get_product_service)
):
    return service.search_products(q, str(category_id) if category_id else None, min_price, max_price, skip, limit)

@router.get("/{id}", response_model=Product)
def get_product(id: UUID, service: ProductService = Depends(get_product_service)):
    product = service.get_product(str(id))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=List[Product])
def list_products(skip: int = 0, limit: int = 10, service: ProductService = Depends(get_product_service)):
    return service.get_all_products(skip, limit)

@router.put("/{id}", response_model=Product)
def update_product(id: UUID, product_in: ProductUpdate, service: ProductService = Depends(get_product_service)):
    category_ids = [str(cid) for cid in product_in.category_ids] if product_in.category_ids is not None else None
    product = service.update_product(str(id), product_in.dict(exclude={"category_ids"}, exclude_unset=True), category_ids)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{id}", status_code=status.HTTP_201_CREATED) # Requirement says 204, will fix in next step
def delete_product(id: UUID, service: ProductService = Depends(get_product_service)):
    # The requirement says 204 No Content, but also 404 if not found.
    # We should return 204 if successful.
    if not service.delete_product(str(id)):
         raise HTTPException(status_code=404, detail="Product not found")
    from fastapi import Response
    return Response(status_code=status.HTTP_204_NO_CONTENT)
