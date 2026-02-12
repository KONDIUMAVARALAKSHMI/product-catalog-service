import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.junction import product_categories

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)

    products = relationship("Product", secondary=product_categories, back_populates="categories")
