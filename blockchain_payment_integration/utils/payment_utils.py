import uuid
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def generate_order_id():
    """Generate a unique order ID using UUID."""
    order_id = str(uuid.uuid4())
    logger.debug("Generated order ID: %s", order_id)
    return order_id

def format_amount(amount, currency):
    """Format the amount for display or API requests."""
    try:
        if currency == "USD":
            formatted = "${:,.2f}".format(Decimal(amount))
        else:
            formatted = "{:,.2f} {}".format(Decimal(amount), currency)
        logger.debug("Formatted amount: %s", formatted)
        return formatted
    except Exception as e:
        logger.error("Error formatting amount: %s", e)
        raise ValueError("Invalid amount format")

def log_payment_event(event_type, payment_data):
    """Log payment events for auditing purposes."""
    logger.info("Payment Event: %s | Data: %s", event_type, payment_data)

def calculate_total_amount(items):
    """Calculate the total amount from a list of items."""
    try:
        total = sum(Decimal(item['price']) * Decimal(item['quantity']) for item in items)
        logger.debug("Calculated total amount: %s", total)
        return total
    except Exception as e:
        logger.error("Error calculating total amount: %s", e)
        raise ValueError("Invalid items for total calculation")

def validate_payment_data(payment_data):
    """Validate payment data structure."""
    required_fields = ['amount', 'currency', 'method']
    for field in required_fields:
        if field not in payment_data:
            logger.error("Missing required field: %s", field)
            raise ValueError(f"Missing required field: {field}")
    logger.debug("Payment data validated: %s", payment_data)
