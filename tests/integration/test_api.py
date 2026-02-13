import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import Base, engine, SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_category():
    response = client.post("/categories/", json={"name": "Integration Test Cat", "description": "Test Desc"})
    assert response.status_code == 201
    return response.json()["id"]

def test_create_category():
    response = client.post("/categories/", json={"name": "Test Cat 2", "description": "Test Desc"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Cat 2"

def test_create_product(test_category):
    response = client.post("/products/", json={
        "name": "Test Prod",
        "description": "Test Desc",
        "price": 99.99,
        "sku": "TEST-SKU-001",
        "category_ids": [test_category]
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Prod"
    assert len(response.json()["categories"]) >= 1

def test_search_products(test_category):
    # Create a product first
    client.post("/products/", json={
        "name": "Searchable Product",
        "description": "Test Desc",
        "price": 49.99,
        "sku": "SEARCH-001",
        "category_ids": [test_category]
    })
    response = client.get("/products/search?q=Searchable")
    assert response.status_code == 200
    assert len(response.json()) >= 1
