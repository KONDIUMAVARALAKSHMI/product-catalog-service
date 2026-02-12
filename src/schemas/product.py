from pydantic import BaseModel, Field, UUID4, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: UUID4
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    sku: str = Field(..., min_length=3)

class ProductCreate(ProductBase):
    category_ids: Optional[List[UUID4]] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    sku: Optional[str] = None
    category_ids: Optional[List[UUID4]] = None

class Product(ProductBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    categories: List[Category] = []

    class Config:
        from_attributes = True

class ProductSearch(BaseModel):
    q: Optional[str] = None
    category_id: Optional[UUID4] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    skip: int = 0
    limit: int = 10
