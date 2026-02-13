import uuid
from sqlalchemy import Column, String, Text, Numeric, TIMESTAMP, Uuid
# form sqlalchemy.dialects.postgresql import UUID # Removed
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base
from src.models.junction import product_categories

class Product(Base):
    __tablename__ = "products"

    id = Column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(Text, nullable=False, index=True)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False, index=True)
    sku = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = relationship("Category", secondary=product_categories, back_populates="products")
