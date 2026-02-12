from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from src.database import get_db
from src.models.product import Product
from src.schemas.product import ProductCreate, ProductResponse
from datetime import datetime

router = APIRouter()

# CREATE
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# GET ALL
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# GET BY ID
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, updated_data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_data.model_dump().items():
        setattr(product, key, value)

    product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product


# DELETE
@router.delete("/{product_id}")
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
