# payment_system/payment_routes.py

from flask import Blueprint, request, jsonify
import stripe

payment_routes = Blueprint('payment_routes', __name__)

# Configure Stripe
stripe.api_key = 'YOUR_STRIPE_SECRET_KEY'  # Replace with your Stripe secret key

@payment_routes.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = request.get_json()
    currency = data['currency']

    # Create PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=1000,  # Amount in cents (e.g., $10.00)
        currency=currency,
        payment_method_types=['card'],
    )

    return jsonify({'clientSecret': intent['client_secret']})
