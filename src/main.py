from fastapi import FastAPI
from src.routes.product import router as product_router
from src.routes.category import router as category_router
from src.database import Base, engine

app = FastAPI(
    title="Product Catalog Service",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])

@app.get("/health")
def health_check():
    return {"status": "UP"}
