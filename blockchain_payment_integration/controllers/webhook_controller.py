from flask import Blueprint, request, jsonify
import logging
import hmac
import hashlib
import os

# Create a blueprint for the webhook controller
webhook_bp = Blueprint('webhook', __name__)
logger = logging.getLogger(__name__)

def verify_coinbase_signature(payload, signature):
    """Verify the Coinbase webhook signature."""
    secret = os.getenv('COINBASE_WEBHOOK_SECRET').encode()
    expected_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

@webhook_bp.route('/api/webhooks/coinbase', methods=['POST'])
def coinbase_webhook():
    """Endpoint to handle Coinbase webhook notifications."""
    payload = request.get_data()
    signature = request.headers.get('X-SIGNATURE')

    if not verify_coinbase_signature(payload, signature):
        logger.warning("Invalid Coinbase webhook signature.")
        return jsonify({"error": "Invalid signature"}), 403

    data = request.json
    logger.info("Received Coinbase webhook: %s", data)

    # Process the webhook event
    event_type = data.get('event', {}).get('type')
    if event_type == 'charge:confirmed':
        logger.info("Charge confirmed: %s", data)
        # TODO: Update payment status in the database
    elif event_type == 'charge:failed':
        logger.warning("Charge failed: %s", data)
        # TODO: Update payment status in the database
    else:
        logger.info("Unhandled event type: %s", event_type)

    return jsonify({"status": "success"}), 200

def verify_bitpay_signature(payload, signature):
    """Verify the BitPay webhook signature."""
    # BitPay uses a different method for signature verification
    # Implement the verification logic based on BitPay's documentation
    # This is a placeholder for the actual implementation
    return True  # Replace with actual verification logic

@webhook_bp.route('/api/webhooks/ bitpay', methods=['POST'])
def bitpay_webhook():
    """Endpoint to handle BitPay webhook notifications."""
    payload = request.get_data()
    signature = request.headers.get('X-SIGNATURE')

    if not verify_bitpay_signature(payload, signature):
        logger.warning("Invalid BitPay webhook signature.")
        return jsonify({"error": "Invalid signature"}), 403

    data = request.json
    logger.info("Received BitPay webhook: %s", data)

    # Process the webhook event
    status = data.get('status')
    if status == 'paid':
        logger.info("Payment received: %s", data)
        # TODO: Update payment status in the database
    elif status == 'failed':
        logger.warning("Payment failed: %s", data)
        # TODO: Update payment status in the database
    else:
        logger.info("Unhandled payment status: %s", status)

    return jsonify({"status": "success"}), 200
