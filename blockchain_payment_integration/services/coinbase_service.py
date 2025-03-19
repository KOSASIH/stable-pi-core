import requests
import logging
import os
from models.payment import Payment, PaymentStatus

logger = logging.getLogger(__name__)

class CoinbaseService:
    def __init__(self):
        self.api_key = os.getenv('COINBASE_API_KEY')
        self.api_url = 'https://api.commerce.coinbase.com/charges'
        self.headers = {
            'Content-Type': 'application/json',
            'X-CC-Api-Key': self.api_key,
            'X-CC-Version': '2018-03-22'
        }

    def create_payment(self, amount, currency):
        """Create a payment using Coinbase Commerce API."""
        payload = {
            "name": "Payment for Order",
            "description": "Order description",
            "local_price": {
                "amount": str(amount),
                "currency": currency
            },
            "pricing_type": "fixed_price",
            "redirect_url": os.getenv('REDIRECT_URL', 'https://your_redirect_url.com'),
            "cancel_url": os.getenv('CANCEL_URL', 'https://your_cancel_url.com')
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            payment_data = response.json()

            # Validate response structure
            if 'data' not in payment_data or 'id' not in payment_data['data']:
                logger.error("Invalid response structure from Coinbase: %s", payment_data)
                raise ValueError("Invalid response from Coinbase API")

            logger.info("Coinbase payment created successfully: %s", payment_data['data'])
            return payment_data['data']
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred while creating payment: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred while creating payment: %s", err)
            raise

    def get_payment_status(self, payment_id):
        """Retrieve the status of a payment."""
        try:
            response = requests.get(f"{self.api_url}/{payment_id}", headers=self.headers)
            response.raise_for_status()
            payment_data = response.json()

            # Validate response structure
            if 'data' not in payment_data:
                logger.error("Invalid response structure from Coinbase: %s", payment_data)
                raise ValueError("Invalid response from Coinbase API")

            logger.info("Retrieved payment status: %s", payment_data['data'])
            return payment_data['data']
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred while retrieving payment status: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred while retrieving payment status: %s", err)
            raise
