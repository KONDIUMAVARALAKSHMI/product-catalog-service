# Product Catalog Service

A robust backend microservice for managing an e-commerce product catalog using Repository Pattern and Unit of Work.

## Features
- **RESTful API**: Manage products and categories with clean endpoints.
- **Repository Pattern**: Abstracted data access layer for better maintainability.
- **Unit of Work**: Managed transactions for data integrity.
- **Advanced Search**: Filter products by keyword, category, and price range.
- **Dockerized**: Easy setup using Docker and Docker Compose.
- **Seeding**: Automatically populates the database with initial products and categories.

## Architecture
- **API Layer**: FastAPI handles request/response and validation (Pydantic).
- **Service Layer**: Business logic orchestrated via Unit of Work.
- **Data Access Layer**: Repositories interact with the database using SQLAlchemy.
- **Database**: PostgreSQL (Docker) or SQLite (Local fallback).

## Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (if running locally without Docker)

### Run with Docker (Recommended)
```bash
docker-compose up --build
```
This will:
1. Start a PostgreSQL database.
2. Build the FastAPI application.
3. Automatically seed the database with 10 products and 3 categories.
4. Expose the API at `http://localhost:8000`.

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run seeding:
   ```bash
   python src/seed.py
   ```
3. Run the app:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Endpoints & Examples

### Products

#### **POST /products/**
Create a new product.
**Request:**
```json
{
  "name": "Mechanical Keyboard",
  "description": "RGB Backlit, Brown Switches",
  "price": 59.99,
  "sku": "KEY-001",
  "category_ids": ["uuid-of-electronics"]
}
```
**Response (201 Created):**
```json
{
  "id": "uuid-pk",
  "name": "Mechanical Keyboard",
  "price": 59.99,
  "sku": "KEY-001",
  "categories": [...]
}
```

#### **GET /products/search**
Advanced search with filters.
**Example Query:** `/products/search?q=Keyboard&min_price=50&category_id=uuid`
**Response (200 OK):** Array of product objects matching criteria.

### Categories

#### **POST /categories/**
**Request:**
```json
{
  "name": "Electronics",
  "description": "Computers and gadgets"
}
```

## Architectural Decisions

### Repository Pattern & Unit of Work
- **IRepository**: Provides a generic interface for CRUD operations, decoupling business logic from the specific ORM/DB implementation.
- **Unit of Work**: Manages the SQLAlchemy session lifecycle and ensures that multiple repository operations (e.g., adding a product and linking its categories) happen within a single atomic transaction.

### Search Strategy
- **Indexing**: Database-level B-Tree indexes are applied to `name` and `price` columns in the `products` table to ensure performant filtering on large datasets.
- **Dynamic Filtering**: The `search` method in `ProductRepository` dynamically builds the SQL query based on provided filters (keyword matching via `ILike`, price ranges, and category relationship checks using `any()`).
- **Pagination**: Results are paginated at the database level using `offset()` and `limit()` to optimize memory usage and response times.

## Testing
Run unit tests using pytest:
```bash
pytest tests/
```

## Repository Link
[GitHub Repository](https://github.com/KONDIUMAVARALAKSHMI/product-catalog-service)
