# payment-service/app.py
from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# In-memory storage for demonstration
payments = []
payment_counter = 1

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "payment-service"}), 200

@app.route('/payments', methods=['GET'])
def get_payments():
    """Retrieve all payments"""
    return jsonify({"payments": payments}), 200

@app.route('/payments', methods=['POST'])
def process_payment():
    """Process a payment"""
    global payment_counter
    
    data = request.get_json()
    
    # Simulate payment processing
    payment = {
        "payment_id": payment_counter,
        "order_id": data.get("order_id"),
        "amount": data.get("amount"),
        "status": "success" if random.random() > 0.1 else "failed",
        "transaction_id": f"TXN{payment_counter:06d}"
    }
    
    payments.append(payment)
    payment_counter += 1
    
    status_code = 200 if payment["status"] == "success" else 400
    return jsonify(payment), status_code

@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Retrieve specific payment by ID"""
    payment = next((p for p in payments if p["payment_id"] == payment_id), None)
    if payment:
        return jsonify(payment), 200
    return jsonify({"error": "Payment not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
