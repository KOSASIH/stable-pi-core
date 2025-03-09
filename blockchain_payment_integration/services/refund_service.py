import requests
import logging
import os

logger = logging.getLogger(__name__)

class RefundService:
    def __init__(self):
        self.coinbase_api_key = os.getenv('COINBASE_API_KEY')
        self.bitpay_api_key = os.getenv('BITPAY_API_KEY')
        self.coinbase_api_url = 'https://api.commerce.coinbase.com/charges'
        self.bitpay_api_url = 'https://bitpay.com/api/invoice'
        self.coinbase_headers = {
            'Content-Type': 'application/json',
            'X-CC-Api-Key': self.coinbase_api_key,
            'X-CC-Version': '2018-03-22'
        }
        self.bitpay_headers = {
            'Content-Type': 'application/json',
            'X-BitPay-Api-Key': self.bitpay_api_key
        }

    def refund_coinbase_payment(self, payment_id, amount):
        """Request a refund for a Coinbase payment."""
        payload = {
            "amount": str(amount),
            "currency": "USD"  # Adjust as necessary
        }
        try:
            response = requests.post(f"{self.coinbase_api_url}/{payment_id}/refund", json=payload, headers=self.coinbase_headers)
            response.raise_for_status()
            refund_data = response.json()
            logger.info("Coinbase refund requested successfully: %s", refund_data)
            return refund_data
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred while requesting Coinbase refund: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred while requesting Coinbase refund: %s", err)
            raise

    def refund_bitpay_payment(self, invoice_id, amount):
        """Request a refund for a BitPay payment."""
        payload = {
            "amount": amount,
            "currency": "USD"  # Adjust as necessary
        }
        try:
            response = requests.post(f"{self.bitpay_api_url}/{invoice_id}/refund", json=payload, headers=self.bitpay_headers)
            response.raise_for_status()
            refund_data = response.json()
            logger.info("BitPay refund requested successfully: %s", refund_data)
            return refund_data
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred while requesting BitPay refund: %s", http_err)
            raise
        except Exception as err:
            logger.error("An error occurred while requesting BitPay refund: %s", err)
            raise
