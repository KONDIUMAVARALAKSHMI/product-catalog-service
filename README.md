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

## API Documentation
Once the application is running, you can access the interactive Swagger UI at:
[http://localhost:8000/docs](http://localhost:8000/docs)

### Endpoints Summary
- `GET /products/search`: Search with filters (`q`, `category_id`, `min_price`, `max_price`, `skip`, `limit`).
- `GET /products`: List all products (paginated).
- `POST /products`: Create a new product.
- `GET /categories`: List all categories.
- `POST /categories`: Create a new category.

## Testing
Run unit tests using pytest:
```bash
pytest tests/
```

## Repository Link
[GitHub Repository](https://github.com/KONDIUMAVARALAKSHMI/product-catalog-service)
