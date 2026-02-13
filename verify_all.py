import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_endpoint(method, endpoint, data=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code == expected_status:
            log(f"{method} {endpoint} - Success ({response.status_code})")
            return response.json() if response.content else None
        else:
            log(f"{method} {endpoint} - Failed ({response.status_code})", "ERROR")
            log(f"Response: {response.text}", "ERROR")
            return None
    except Exception as e:
        log(f"{method} {endpoint} - Exception: {e}", "ERROR")
        return None

# 1. Categories
log("--- Testing Categories ---")
unique_name = f"Test-{uuid.uuid4()}"
cat_data = {"name": unique_name, "description": "Test Desc"}
cat = test_endpoint("POST", "/categories/", cat_data, 201)

if cat:
    cat_id = cat["id"]
    test_endpoint("GET", f"/categories/{cat_id}", expected_status=200)
    
    update_data = {"name": "Updated Category", "description": "Updated Desc"}
    test_endpoint("PUT", f"/categories/{cat_id}", update_data, 200)
    
    test_endpoint("DELETE", f"/categories/{cat_id}", expected_status=204)
    test_endpoint("GET", f"/categories/{cat_id}", expected_status=404)

# 2. Products
log("\n--- Testing Products ---")
# Need a category first
unique_cat = f"Elec-{uuid.uuid4()}"
electronics = test_endpoint("POST", "/categories/", {"name": unique_cat, "description": "Tech"}, 201)
if electronics:
    elec_id = electronics["id"]
    
    prod_data = {
        "name": "Test Product", 
        "description": "Desc", 
        "price": 100.0, 
        "sku": f"TEST-{uuid.uuid4()}", 
        "category_ids": [elec_id]
    }
    prod = test_endpoint("POST", "/products/", prod_data, 201)
    
    if prod:
        prod_id = prod["id"]
        test_endpoint("GET", f"/products/{prod_id}", expected_status=200)
        
        update_prod = {"price": 150.0}
        test_endpoint("PUT", f"/products/{prod_id}", update_prod, 200)
        
        # Search
        test_endpoint("GET", "/products/search?q=Test", expected_status=200)
        
        test_endpoint("DELETE", f"/products/{prod_id}", expected_status=204)
        test_endpoint("GET", f"/products/{prod_id}", expected_status=404)

log("\n--- Testing Completed ---")
