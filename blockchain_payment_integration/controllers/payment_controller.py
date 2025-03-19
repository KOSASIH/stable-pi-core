from flask import Blueprint, request, jsonify
from services.coinbase_service import CoinbaseService
from services.bitpay_service import BitPayService
import logging

# Create a blueprint for the payment controller
payment_bp = Blueprint('payment', __name__)
logger = logging.getLogger(__name__)

@payment_bp.route('/api/payments', methods=['POST'])
def create_payment():
    """Endpoint to create a new payment."""
    data = request.json
    payment_method = data.get('method')
    amount = data.get('amount')
    currency = data.get('currency')

    # Validate input data
    if not payment_method or not amount or not currency:
        logger.error("Invalid payment request: %s", data)
        return jsonify({"error": "Missing required fields"}), 400

    try:
        if payment_method == 'coinbase':
            service = CoinbaseService()
            payment_response = service.create_payment(amount, currency)
        elif payment_method == 'bitpay':
            service = BitPayService()
            payment_response = service.create_payment(amount, currency)
        else:
            logger.error("Unsupported payment method: %s", payment_method)
            return jsonify({"error": "Unsupported payment method"}), 400

        logger.info("Payment created successfully: %s", payment_response)
        return jsonify(payment_response), 201

    except ValueError as ve:
        logger.error("Value error: %s", ve)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.exception("Error creating payment: %s", e)
        return jsonify({"error": "Internal server error"}), 500

@payment_bp.route('/api/payments/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    """Endpoint to get the status of a payment."""
    try:
        service = CoinbaseService()  # or BitPayService() based on your logic
        payment_status = service.get_payment_status(payment_id)

        if payment_status is None:
            logger.warning("Payment not found: %s", payment_id)
            return jsonify({"error": "Payment not found"}), 404

        logger.info("Payment status retrieved: %s", payment_status)
        return jsonify(payment_status), 200

    except Exception as e:
        logger.exception("Error retrieving payment status: %s", e)
        return jsonify({"error": "Internal server error"}), 500
