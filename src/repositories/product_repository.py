from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.product import Product
from src.repositories.base_repository import IRepository

class IProductRepository(IRepository[Product]):
    @abstractmethod
    def search(self, q: Optional[str] = None, category_id: Optional[str] = None, 
               min_price: Optional[float] = None, max_price: Optional[float] = None, 
               skip: int = 0, limit: int = 10) -> List[Product]:
        pass

class ProductRepository(IProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, item_id: str) -> Optional[Product]:
        return self.session.query(Product).filter(Product.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.session.query(Product).offset(skip).limit(limit).all()

    def add(self, item: Product) -> Product:
        self.session.add(item)
        return item

    def update(self, item_id: str, item: Product) -> Optional[Product]:
        db_item = self.get_by_id(item_id)
        if db_item:
            for key, value in item.__dict__.items():
                if not key.startswith('_') and key != 'id':
                    setattr(db_item, key, value)
            return db_item
        return None

    def delete(self, item_id: str) -> bool:
        db_item = self.get_by_id(item_id)
        if db_item:
            self.session.delete(db_item)
            return True
        return False

    def search(self, q: Optional[str] = None, category_id: Optional[str] = None, 
               min_price: Optional[float] = None, max_price: Optional[float] = None, 
               skip: int = 0, limit: int = 10) -> List[Product]:
        query = self.session.query(Product)
        
        if q:
            query = query.filter(
                (Product.name.ilike(f"%{q}%")) | 
                (Product.description.ilike(f"%{q}%"))
            )
        
        if category_id:
            query = query.filter(Product.categories.any(id=category_id))
            
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
            
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
            
        return query.offset(skip).limit(limit).all()

from abc import abstractmethod # Adding this for IProductRepository
