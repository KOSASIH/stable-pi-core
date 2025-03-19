import re
import logging

logger = logging.getLogger(__name__)

def validate_amount(amount):
    """Validate that the amount is a positive number."""
    if not isinstance(amount, (int, float, Decimal)) or amount <= 0:
        logger.error("Invalid amount: %s", amount)
        raise ValueError("Amount must be a positive number.")
    logger.debug("Validated amount: %s", amount)
    return True

def validate_currency(currency):
    """Validate that the currency is a valid ISO 4217 code."""
    if not isinstance(currency, str) or len(currency) != 3 or not currency.isalpha():
        logger.error("Invalid currency code: %s", currency)
        raise ValueError("Currency must be a 3-letter ISO code.")
    logger.debug("Validated currency: %s", currency)
    return currency.upper()

def validate_email(email):
    """Validate that the email address is in a valid format."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        logger.error("Invalid email address format: %s", email)
        raise ValueError("Invalid email address format.")
    logger.debug("Validated email: %s", email)
    return email

def validate_payment_method(method):
    """Validate that the payment method is supported."""
    supported_methods = ['coinbase', 'bitpay']
    if method not in supported_methods:
        logger.error("Unsupported payment method: %s", method)
        raise ValueError(f"Unsupported payment method: {method}. Supported methods: {supported_methods}")
    logger.debug("Validated payment method: %s", method)
    return method

def validate_transaction_data(transaction_data):
    """Validate transaction data structure."""
    required_fields = ['transaction_id', 'amount', 'currency', 'status']
    for field in required_fields:
        if field not in transaction_data:
            logger.error("Missing required field in transaction data: %s", field)
            raise ValueError(f"Missing required field in transaction data: {field}")
    logger.debug("Transaction data validated: %s", transaction_data)
