# order-service/app.py
from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

# In-memory storage for demonstration
orders = []
order_counter = 1

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "order-service"}), 200

@app.route('/orders', methods=['GET'])
def get_orders():
    """Retrieve all orders"""
    return jsonify({"orders": orders}), 200

@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order and initiate payment"""
    global order_counter
    
    data = request.get_json()
    order = {
        "order_id": order_counter,
        "customer_name": data.get("customer_name"),
        "item": data.get("item"),
        "quantity": data.get("quantity", 1),
        "amount": data.get("amount"),
        "status": "pending"
    }
    
    # Call payment service
    payment_service_url = os.getenv("PAYMENT_SERVICE_URL", "http://payment-service:5001")
    try:
        payment_response = requests.post(
            f"{payment_service_url}/payments",
            json={"order_id": order_counter, "amount": order["amount"]},
            timeout=5
        )
        if payment_response.status_code == 200:
            order["status"] = "confirmed"
            order["payment_id"] = payment_response.json().get("payment_id")
    except Exception as e:
        order["status"] = "payment_failed"
        order["error"] = str(e)
    
    orders.append(order)
    order_counter += 1
    
    return jsonify(order), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieve specific order by ID"""
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if order:
        return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
