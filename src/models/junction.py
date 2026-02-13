from sqlalchemy import Table, Column, ForeignKey, Uuid # Added Uuid
# from sqlalchemy.dialects.postgresql import UUID # Removed
from src.database import Base

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", Uuid(as_uuid=False), ForeignKey("products.id"), primary_key=True),
    Column("category_id", Uuid(as_uuid=False), ForeignKey("categories.id"), primary_key=True),
)
