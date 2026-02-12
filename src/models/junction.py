from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True),
    Column("category_id", UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True),
)
