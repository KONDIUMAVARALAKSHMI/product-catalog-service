from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.category import Category
from src.repositories.base_repository import IRepository

class ICategoryRepository(IRepository[Category]):
    pass

class CategoryRepository(ICategoryRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, item_id: str) -> Optional[Category]:
        return self.session.query(Category).filter(Category.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.session.query(Category).offset(skip).limit(limit).all()

    def add(self, item: Category) -> Category:
        self.session.add(item)
        return item

    def update(self, item_id: str, item: Category) -> Optional[Category]:
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
