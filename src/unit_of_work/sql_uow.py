from sqlalchemy.orm import Session
from src.unit_of_work.base_uow import IUnitOfWork
from src.repositories.product_repository import ProductRepository, IProductRepository
from src.repositories.category_repository import CategoryRepository, ICategoryRepository

class SqlUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session = None
        self._products = None
        self._categories = None

    @property
    def products(self) -> IProductRepository:
        if self._products is None:
            self._products = ProductRepository(self._session)
        return self._products

    @property
    def categories(self) -> ICategoryRepository:
        if self._categories is None:
            self._categories = CategoryRepository(self._session)
        return self._categories

    def begin(self):
        self._session = self.session_factory()
        self._products = None
        self._categories = None

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

    def dispose(self):
        if self._session:
            self._session.close()
            self._session = None
            self._products = None
            self._categories = None
