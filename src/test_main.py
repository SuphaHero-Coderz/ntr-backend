import time
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_create_order():
    NUM_TOKENS = 5

    order_info = {
        "num_tokens": NUM_TOKENS
    }
    response = client.post("/create-order", json=order_info)
    
    assert response.status_code == 201
    assert response.json() == {
        "message": "Order created"    
    }
    
    time.sleep(5)

    response = client.get("/get-orders", params={"user_id" : 1})
    assert response.status_code == 200
    orders = response.json()
    created_order = orders[0]

    assert created_order["id"] == 1
    assert created_order["user_id"] == 1
    assert created_order["status_message"] == "Order complete"
    assert created_order["status"] == "complete"
    assert created_order["num_tokens"] == NUM_TOKENS
