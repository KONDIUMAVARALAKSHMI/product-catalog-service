from abc import ABC, abstractmethod
from src.repositories.product_repository import IProductRepository
from src.repositories.category_repository import ICategoryRepository

class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def products(self) -> IProductRepository:
        pass

    @property
    @abstractmethod
    def categories(self) -> ICategoryRepository:
        pass

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def dispose(self):
        pass
