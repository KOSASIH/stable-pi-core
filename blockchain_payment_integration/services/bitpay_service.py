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
            "notificationURL": "https://your_notification_url.com",
            "redirectURL": "https://your_redirect_url.com",
            "orderId": "order_id_here",
            "itemDesc": "Payment for Order"
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            payment_data = response.json()
            logger.info("BitPay payment created successfully: %s", payment_data)
            return payment_data
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred: %s", err)
            raise

    def get_payment_status(self, invoice_id):
        """Retrieve the status of a payment."""
        try:
            response = requests.get(f"{self.api_url}/{invoice_id}", headers=self.headers)
            response.raise_for_status()
            payment_data = response.json()
            logger.info("Retrieved payment status: %s", payment_data)
            return payment_data
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred: %s", err)
            raise
