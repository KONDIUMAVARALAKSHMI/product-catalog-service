from typing import List, Optional
from src.unit_of_work.base_uow import IUnitOfWork
from src.models.category import Category

class CategoryService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def create_category(self, category_data: dict) -> Category:
        self.uow.begin()
        try:
            category = Category(
                name=category_data["name"],
                description=category_data.get("description")
            )
            self.uow.categories.add(category)
            self.uow.commit()
            # Ensure attributes are loaded before session potentially closes
            return category
        except Exception as e:
            self.uow.rollback()
            raise e
        finally:
            self.uow.dispose()

    def get_category(self, category_id: str) -> Optional[Category]:
        self.uow.begin()
        try:
            return self.uow.categories.get_by_id(category_id)
        finally:
            self.uow.dispose()

    def get_all_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        self.uow.begin()
        try:
            return self.uow.categories.get_all(skip, limit)
        finally:
            self.uow.dispose()

    def update_category(self, category_id: str, category_data: dict) -> Optional[Category]:
        self.uow.begin()
        try:
            existing_category = self.uow.categories.get_by_id(category_id)
            if not existing_category:
                return None
            
            for key, value in category_data.items():
                if hasattr(existing_category, key):
                    setattr(existing_category, key, value)
            
            self.uow.commit()
            return existing_category
        except Exception as e:
            self.uow.rollback()
            raise e
        finally:
            self.uow.dispose()

    def delete_category(self, category_id: str) -> bool:
        self.uow.begin()
        try:
            result = self.uow.categories.delete(category_id)
            self.uow.commit()
            return result
        except Exception as e:
            self.uow.rollback()
            raise e
        finally:
            self.uow.dispose()
