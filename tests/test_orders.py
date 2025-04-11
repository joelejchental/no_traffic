import requests
import pytest
from conftest import ORDER_ID

# 1. Test Create Order
def test_create_order(api_base_url, mock_api):
    response = requests.post(api_base_url, json={"user_id": "u12345", "items": [{"product_id": "p001", "name": "Laptop", "price": 1200, "quantity": 1}]})
    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json["_id"] == ORDER_ID
    assert resp_json["status"] == "Pending"

# 2. Test Get Order by ID
def test_get_order(api_base_url, mock_api):
    response = requests.get(f"{api_base_url}/{ORDER_ID}")
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["_id"] == ORDER_ID
    assert resp_json["status"] == "Pending"

# 3. Test Update Order Status
@pytest.mark.parametrize("new_status", ["Pending", "Shipped", "Delivered"])
def test_update_order_status(api_base_url, mock_api, new_status):
    response = requests.patch(f"{api_base_url}/{ORDER_ID}", json={"status": new_status})
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["message"] == "Order updated"

# 4. Test Delete Order
def test_delete_order(api_base_url, mock_api):
    response = requests.delete(f"{api_base_url}/{ORDER_ID}")
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["message"] == "Order deleted"

# 5. Test Get Order After Deletion
def test_get_order_after_delete(api_base_url, mock_api):
    # Delete the order first
    requests.delete(f"{api_base_url}/{ORDER_ID}")
    # Try to get it after deletion
    response = requests.get(f"{api_base_url}/{ORDER_ID}")
    assert response.status_code == 404
    resp_json = response.json()
    assert resp_json["error"] == "Order not found"
