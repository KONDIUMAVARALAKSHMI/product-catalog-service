import requests

BASE_URL = "http://localhost:8000"

# Create a category
resp = requests.post(f"{BASE_URL}/categories/", json={"name": "DebugCat", "description": "Debug"})
if resp.status_code == 201:
    cat_id = resp.json()["id"]
    print(f"Created category {cat_id}")
    
    # Try to update
    resp = requests.put(f"{BASE_URL}/categories/{cat_id}", json={"name": "UpdatedCat"})
    print(f"Update status: {resp.status_code}")
    print(f"Update response: {resp.text}")
else:
    print(f"Failed to create category: {resp.text}")
