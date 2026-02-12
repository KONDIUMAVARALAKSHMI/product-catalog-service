from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    sku: str

class ProductResponse(ProductCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
