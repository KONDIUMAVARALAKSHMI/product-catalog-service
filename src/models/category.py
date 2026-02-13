import uuid
from sqlalchemy import Column, String, Text, Uuid
# from sqlalchemy.dialects.postgresql import UUID # Removed
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.junction import product_categories

class Category(Base):
    __tablename__ = "categories"

    id = Column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)

    products = relationship("Product", secondary=product_categories, back_populates="categories")
