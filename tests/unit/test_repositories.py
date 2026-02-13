import pytest
from unittest.mock import MagicMock
from src.repositories.product_repository import ProductRepository
from src.models.product import Product

def test_product_repository_get_by_id():
    # Mock SQLAlchemy Session
    mock_session = MagicMock()
    repo = ProductRepository(mock_session)
    
    # Mocking query chain with options and joinedload
    mock_query = mock_session.query.return_value
    mock_options = mock_query.options.return_value
    mock_filter = mock_options.filter.return_value
    mock_filter.first.return_value = Product(id="some-id", name="Test Product", price=99.99, sku="TEST-001")
    
    result = repo.get_by_id("some-id")
    
    assert result.name == "Test Product"
    mock_session.query.assert_called_once_with(Product)

def test_product_repository_add():
    mock_session = MagicMock()
    repo = ProductRepository(mock_session)
    product = Product(name="New Product", price=49.99, sku="NEW-001")
    
    repo.add(product)
    
    mock_session.add.assert_called_once_with(product)
