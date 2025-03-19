import requests
import logging
import os
from models.payment import Payment, PaymentStatus

logger = logging.getLogger(__name__)

class BitPayService:
    def __init__(self):
        self.api_key = os.getenv('BITPAY_API_KEY')
        self.api_url = 'https://bitpay.com/api/invoice'
        self.headers = {
            'Content-Type': 'application/json',
            'X-BitPay-Plugin-Info': 'Your Plugin Info',
            'X-BitPay-Api-Key': self.api_key
        }

    def create_payment(self, amount, currency):
        """Create a payment using BitPay API."""
        payload = {
            "price": amount,
            "currency": currency,
            "notificationURL": os.getenv('NOTIFICATION_URL', 'https://your_notification_url.com'),
            "redirectURL": os.getenv('REDIRECT_URL', 'https://your_redirect_url.com'),
            "orderId": "order_id_here",  # Replace with a unique order ID
            "itemDesc": "Payment for Order"
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            payment_data = response.json()

            # Validate response structure
            if 'data' not in payment_data or 'id' not in payment_data['data']:
                logger.error("Invalid response structure from BitPay: %s", payment_data)
                raise ValueError("Invalid response from BitPay API")

            logger.info("BitPay payment created successfully: %s", payment_data['data'])
            return payment_data['data']
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred while creating payment: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred while creating payment: %s", err)
            raise

    def get_payment_status(self, invoice_id):
        """Retrieve the status of a payment."""
        try:
            response = requests.get(f"{self.api_url}/{invoice_id}", headers=self.headers)
            response.raise_for_status()
            payment_data = response.json()

            # Validate response structure
            if 'data' not in payment_data:
                logger.error("Invalid response structure from BitPay: %s", payment_data)
                raise ValueError("Invalid response from BitPay API")

            logger.info("Retrieved payment status: %s", payment_data['data'])
            return payment_data['data']
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred while retrieving payment status: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred while retrieving payment status: %s", err)
            raise

    def refund_payment(self, invoice_id, amount):
        """Request a refund for a payment."""
        payload = {
            "amount": amount,
            "currency": "USD",  # Adjust as necessary
            "invoiceId": invoice_id
        }

        try:
            response = requests.post(f"{self.api_url}/{invoice_id}/refund", json=payload, headers=self.headers)
            response.raise_for_status()
            refund_data = response.json()

            # Validate response structure
            if 'data' not in refund_data or 'id' not in refund_data['data']:
                logger.error("Invalid response structure from BitPay refund: %s", refund_data)
                raise ValueError("Invalid response from BitPay API for refund")

            logger.info("Refund requested successfully: %s", refund_data['data'])
            return refund_data['data']
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred while requesting refund: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred while requesting refund: %s", err)
            raise
