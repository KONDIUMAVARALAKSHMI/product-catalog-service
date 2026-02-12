from typing import List, Optional
from src.unit_of_work.base_uow import IUnitOfWork
from src.models.product import Product

class ProductService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def create_product(self, product_data: dict, category_ids: List[str] = None) -> Product:
        self.uow.begin()
        try:
            product = Product(
                name=product_data["name"],
                description=product_data.get("description"),
                price=product_data["price"],
                sku=product_data["sku"]
            )
            if category_ids:
                for cat_id in category_ids:
                    category = self.uow.categories.get_by_id(cat_id)
                    if category:
                        product.categories.append(category)
            
            self.uow.products.add(product)
            self.uow.commit()
            return product
        except Exception as e:
            self.uow.rollback()
            raise e
        finally:
            self.uow.dispose()

    def get_product(self, product_id: str) -> Optional[Product]:
        self.uow.begin()
        try:
            return self.uow.products.get_by_id(product_id)
        finally:
            self.uow.dispose()

    def get_all_products(self, skip: int = 0, limit: int = 10) -> List[Product]:
        self.uow.begin()
        try:
            return self.uow.products.get_all(skip, limit)
        finally:
            self.uow.dispose()

    def update_product(self, product_id: str, product_data: dict, category_ids: List[str] = None) -> Optional[Product]:
        self.uow.begin()
        try:
            # Note: This is a simplified update. Usually you'd use a schema/DTO.
            existing_product = self.uow.products.get_by_id(product_id)
            if not existing_product:
                return None
            
            for key, value in product_data.items():
                if hasattr(existing_product, key):
                    setattr(existing_product, key, value)
            
            if category_ids is not None:
                existing_product.categories = []
                for cat_id in category_ids:
                    category = self.uow.categories.get_by_id(cat_id)
                    if category:
                        existing_product.categories.append(category)
            
            self.uow.commit()
            return existing_product
        except Exception as e:
            self.uow.rollback()
            raise e
        finally:
            self.uow.dispose()

    def delete_product(self, product_id: str) -> bool:
        self.uow.begin()
        try:
            result = self.uow.products.delete(product_id)
            self.uow.commit()
            return result
        except Exception as e:
            self.uow.rollback()
            raise e
        finally:
            self.uow.dispose()

    def search_products(self, q: str = None, category_id: str = None, 
                        min_price: float = None, max_price: float = None, 
                        skip: int = 0, limit: int = 10) -> List[Product]:
        self.uow.begin()
        try:
            return self.uow.products.search(q, category_id, min_price, max_price, skip, limit)
        finally:
            self.uow.dispose()
