import requests
import json

# Cấu hình API
SHOPIFY_STORE_URL = "https://test-store-clover.myshopify.com"
ACCESS_TOKEN = "xxx"


HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# Tạo metafield
def create_product_metafield(product_id, namespace, key, value, value_type):
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-07/products/{product_id}/metafields.json"
    payload = {
        "metafield": {
            "namespace": namespace,
            "key": key,
            "type": value_type,
            "value": value
        }
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        print("Product Metafield created successfully:", response.json())
        return response.json().get("metafield")
    else:
        print("Failed to create product metafield:", response.status_code, response.text)
        return None

# Cập nhật metafield
def update_product_metafield(product_id, metafield_id, new_value, value_type):
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-07/products/{product_id}/metafields/{metafield_id}.json"
    payload = {
        "metafield": {
            "id": metafield_id,
            "value": new_value,
            "type": value_type
        }
    }
    
    response = requests.put(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("Product Metafield updated successfully:", response.json())
    else:
        print("Failed to update product metafield:", response.status_code, response.text)

# Lấy danh sách tất cả metafield của sản phẩm
def get_product_metafields(product_id):
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-07/products/{product_id}/metafields.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print("Product Metafields fetched successfully")
        return response.json().get("metafields", [])
    else:
        print("Failed to fetch product metafields:", response.status_code, response.text)
        return []

if __name__ == "__main__":
    product_id = 8191466471585

    # Bước 1: Tạo metafield
    metafield = create_product_metafield(
        product_id=product_id,
        namespace="my_fields",
        key="sponsor",
        value="Shopify",
        value_type="single_line_text_field"
    )

    # Bước 2: Cập nhật metafield 
    if metafield:
        update_product_metafield(
            product_id=product_id,
            metafield_id=metafield["id"],
            new_value="Updated Value",
            value_type="single_line_text_field"
        )

    # Bước 3: Lấy tất cả metafields và hiển thị
    metafields = get_product_metafields(product_id)
    for mf in metafields:
        print(f"Metafield ID: {mf['id']}, Key: {mf['key']}, Value: {mf['value']}")