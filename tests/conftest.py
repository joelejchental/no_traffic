# conftest.py
import pytest
import requests_mock

fake_url = "http://mocked-api.local/orders"
ORDER_ID = "65fd8a1b1234567890abcd12"

@pytest.fixture(scope="session")
def api_base_url():
    return fake_url

@pytest.fixture(scope="function")
def mock_api(api_base_url):
    with requests_mock.Mocker() as mock:
        # Store dynamic order data here
        order_data = {
            "_id": ORDER_ID,
            "status": "Pending"
        }

        # CREATE
        mock.post(api_base_url, json=order_data, status_code=201)

        # GET - Always returns current order data if exists
        def get_order_callback(request, context):
            if order_data:
                return order_data
            context.status_code = 404
            return {"error": "Order not found"}

        mock.get(f"{api_base_url}/{ORDER_ID}", json=get_order_callback)

        # PATCH - Update order status dynamically
        def patch_order_callback(request, context):
            payload = request.json()
            if "status" in payload:
                order_data["status"] = payload["status"]
            return {"message": "Order updated"}

        mock.patch(f"{api_base_url}/{ORDER_ID}", json=patch_order_callback)

        # DELETE - Clear order data to simulate deletion
        def delete_order_callback(request, context):
            order_data.clear()
            return {"message": "Order deleted"}

        mock.delete(f"{api_base_url}/{ORDER_ID}", json=delete_order_callback)

        yield mock
