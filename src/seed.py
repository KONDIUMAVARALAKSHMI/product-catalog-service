import uuid
from decimal import Decimal
from src.database import SessionLocal, Base, engine
from src.models.product import Product
from src.models.category import Category

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Category).first():
        print("Database already seeded.")
        db.close()
        return

    # Create Categories
    electronics = Category(name="Electronics", description="Gadgets and tech")
    clothing = Category(name="Clothing", description="Apparel and fashion")
    home = Category(name="Home & Garden", description="Furniture and decor")
    
    db.add_all([electronics, clothing, home])
    db.commit()
    
    # Create Products
    products_data = [
        {"name": "Smartphone", "price": Decimal("699.99"), "sku": "ELEC-001", "categories": [electronics]},
        {"name": "Laptop", "price": Decimal("1299.99"), "sku": "ELEC-002", "categories": [electronics]},
        {"name": "Headphones", "price": Decimal("199.99"), "sku": "ELEC-003", "categories": [electronics]},
        {"name": "T-Shirt", "price": Decimal("19.99"), "sku": "CLOT-001", "categories": [clothing]},
        {"name": "Jeans", "price": Decimal("49.99"), "sku": "CLOT-002", "categories": [clothing]},
        {"name": "Jacket", "price": Decimal("89.99"), "sku": "CLOT-003", "categories": [clothing]},
        {"name": "Coffee Maker", "price": Decimal("79.99"), "sku": "HOME-001", "categories": [home]},
        {"name": "Desk Lamp", "price": Decimal("29.99"), "sku": "HOME-002", "categories": [home]},
        {"name": "Vase", "price": Decimal("15.99"), "sku": "HOME-003", "categories": [home]},
        {"name": "Monitor", "price": Decimal("249.99"), "sku": "ELEC-004", "categories": [electronics]},
    ]
    
    for p_data in products_data:
        cats = p_data.pop("categories")
        product = Product(**p_data)
        product.categories.extend(cats)
        db.add(product)
        
    db.commit()
    print("Database seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed_database()
