import requests
import time

# Cấu hình API
SHOPIFY_STORE_URL = "https://test-store-clover.myshopify.com"
ACCESS_TOKEN = "XXX"

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# Tạo Smart Collection
def create_smart_collection():
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/smart_collections.json"
    payload = {
        "smart_collection": {
            "title": "winter",
            "rules": [
                {"column": "vendor", "relation": "equals", "condition": "test_store_clover"}
            ],
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("Smart Collection:", response.json())
    return response.json()["smart_collection"]["id"]

# Tạo Custom Collection
def create_custom_collection():
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/custom_collections.json"
    payload = {"custom_collection":
                {"title": "Custom Collection winter",
                 "collects": [
                     {
                         "product_id": 8171296293025
                     }
                 ]
                }}
    response = requests.post(url, headers=HEADERS, json=payload)
    print("Custom Collection:", response.json())
    return response.json()["custom_collection"]["id"]

# Tạo Product không option
def create_simple_product():
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/products.json"
    payload = {
        "product": {
            "title": "test simple product",
            "body_html": "<strong>Good snowboard!</strong>",
            "variants": [
                {
                    "price": "10.00",
                    "inventory_management": "shopify",
                }
            ]
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("Simple Product:", response.json())
    return response.json()["product"]["id"]

# Tạo Product có 2 options (Size, Color)
def create_variant_product():
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/products.json"
    payload = {
        "product": {
            "title": "New Product with Variants",
            "body_html": "This is a product with Size and Color options.",
            "variants": [
                {"option1": "Small", "option2": "Red", "price": "15.00"},
                {"option1": "Large", "option2": "Blue", "price": "20.00"}
            ],
            "options": [
                {"name": "Size", "values": ["Small", "Large"]},
                {"name": "Color", "values": ["Red", "Blue"]}
            ]
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:  # Kiểm tra nếu sản phẩm được tạo thành công
        product_data = response.json()["product"]
        product_id = product_data["id"]
        variants = product_data["variants"]  # Danh sách các variants
        variant_ids = [variant["id"] for variant in variants]  # Trích xuất variant_id
        print(f"Created Product with Variants: {variant_ids}")
        return variant_ids, product_id
    else:
        print(f"Failed to create product: {response.status_code}, {response.json()}")
        return None

# Tạo Customer
def create_customer():
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/customers.json"
    payload = {"customer":
               {"first_name":"Steve",
                "last_name":"Lastnameson",
                "email":"nguyentheduc9alacve+5@gmail.com",
                "phone":"+15142546011",
                "verified_email":True,
                "addresses":[
                    {"address1":"123 Oak St",
                     "city":"Ottawa",
                     "province":"ON",
                     "phone":"555-1212",
                     "zip":"123 ABC",
                     "last_name":"Lastnameson",
                     "first_name":"Mother",
                     "country":"CA"
                     }
                ],
                "password":"newpass",
                "password_confirmation":"newpass",
                "send_email_welcome":False}}
    response = requests.post(url, headers=HEADERS, json=payload)
    print("Customer:", response.json())
    return response.json()["customer"]["id"]

# Tạo Order
def create_order(customer_id, variant_id):
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/orders.json"
    payload = {
        "order": {
            "line_items": [{"variant_id": variant_id, "quantity": 1}],
            "customer": {"id": customer_id}
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    print("Order Response:", response.json())

    # Kiểm tra lỗi trong response trước khi truy cập dữ liệu
    if "order" in response.json():
        return response.json()["order"]["id"]
    else:
        print("Order creation failed:", response.json())
        return None

# Cập nhật giá Product
def update_price(variant_id, new_price):
    # Sử dụng endpoint variants để cập nhật giá
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/variants/{variant_id}.json"
    payload = {
        "variant": {
            "id": variant_id,
            "price": new_price
        }
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    print("Updated Price Response:", response.json())

    if response.status_code == 200:
        print("Price updated successfully!")
    else:
        print("Failed to update price:", response.status_code, response.json())

# Cập nhật ảnh Product
def update_image(product_id, image_url):
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/products/{product_id}/images.json"
    payload = {"image": {"src": image_url}}
    response = requests.post(url, headers=HEADERS, json=payload)
    print("Updated Image:", response.json())

def get_location_id():
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/locations.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        locations = response.json()["locations"]
        return locations[0]["id"]  # Trả về location đầu tiên
    else:
        print("Failed to fetch locations:", response.json())
        return None
    
def update_inventory_quantity(inventory_item_id, location_id, new_quantity):
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/inventory_levels/set.json"
    payload = {
        "inventory_item_id": inventory_item_id,
        "location_id": location_id,
        "available": new_quantity
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f"Inventory updated successfully for inventory_item_id {inventory_item_id} to {new_quantity}.")
    else:
        print("Failed to update inventory:", response.status_code, response.json())

def update_quantity(product_id=None, variant_id=None, new_quantity=0):
    """
    Cập nhật số lượng tồn kho cho sản phẩm thường hoặc sản phẩm có biến thể.
    - Sử dụng product_id cho sản phẩm thường.
    - Sử dụng variant_id cho sản phẩm có biến thể.
    """
    # Nếu sử dụng product_id
    if product_id and not variant_id:
        print(f"Fetching inventory_item_id for product_id: {product_id}")
        # Lấy thông tin sản phẩm
        url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/products/{product_id}.json"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200 or response.status_code == 201:
            product_data = response.json()
            variants = product_data["product"]["variants"]
            if len(variants) == 1:  # Chỉ có một variant
                inventory_item_id = variants[0]["inventory_item_id"]
            else:
                print("This product has multiple variants. Use variant_id instead.")
                return
        else:
            print(f"Failed to fetch product with product_id {product_id}: {response.json()}")
            return

    # Nếu sử dụng variant_id
    elif variant_id:
        print(f"Using variant_id: {variant_id}")
        # Lấy inventory_item_id từ variant_id
        url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/variants/{variant_id}.json"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            inventory_item_id = response.json()["variant"]["inventory_item_id"]
        else:
            print(f"Failed to fetch variant with variant_id {variant_id}: {response.json()}")
            return
    else:
        print("Either product_id or variant_id must be provided.")
        return

    # Lấy location_id
    location_id = get_location_id()
    if not location_id:
        print("Failed to fetch location_id.")
        return

    # Cập nhật số lượng tồn kho
    update_inventory_quantity(inventory_item_id, location_id, new_quantity)

# Xóa dữ liệu
def delete_entity(entity_type, entity_id):
    # Xử lý endpoint đặc biệt cho khách hàng
    if entity_type == "customers":
        url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/customers/{entity_id}.json"
    else:
        url = f"{SHOPIFY_STORE_URL}/admin/api/2024-10/{entity_type}/{entity_id}.json"
    
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Deleted {entity_type.capitalize()} (ID: {entity_id}) successfully.")
    elif response.status_code == 406:
        print(f"Failed to delete {entity_type.capitalize()} (ID: {entity_id}): Shopify does not allow direct deletion.")
    else:
        print(f"Failed to delete {entity_type.capitalize()} (ID: {entity_id}), Status Code: {response.status_code}, Response: {response.json()}")


# Chương trình chính
def main():
    # Tạo dữ liệu
    smart_collection_id = create_smart_collection()
    custom_collection_id = create_custom_collection()
    simple_product_id = create_simple_product()
    variant_ids, product_id = create_variant_product()
    variant_id = variant_ids[0]
    customer_id = create_customer()

    order_id = create_order(customer_id, variant_id)
    
    # Cập nhật dữ liệu
    update_price(variant_id, "12.00")
    update_image(simple_product_id, "https://img.thuthuatphanmem.vn/uploads/2018/09/26/hinh-nen-chu-meo-con-giua-nhung-bong-hoa-dep_053030421.jpg")
    update_quantity(product_id=simple_product_id, new_quantity=50)

    # Xóa toàn bộ dữ liệu
    delete_entity("smart_collections", smart_collection_id)
    delete_entity("custom_collections", custom_collection_id)
    delete_entity("products", simple_product_id)
    delete_entity("products", product_id)
    delete_entity("orders", order_id)
    time.sleep(10)
    delete_entity("customers", customer_id)
    
if __name__ == "__main__":
    main()