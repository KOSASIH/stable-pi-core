import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def format_timestamp(timestamp):
    """
    Format a timestamp into a human-readable string.
    
    :param timestamp: The timestamp to format.
    :return: Formatted timestamp string.
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def validate_transaction_data(transaction):
    """
    Validate the data of a transaction.
    
    :param transaction: The transaction data to validate.
    :return: Boolean indicating validity.
    """
    if 'sender' not in transaction or 'receiver' not in transaction:
        logging.warning("Transaction must have sender and receiver.")
        return False
    if transaction['amount'] <= 0:
        logging.warning("Transaction amount must be greater than zero.")
        return False
    return True

def log_transaction(transaction):
    """
    Log the details of a transaction.
    
    :param transaction: The transaction to log.
    """
    logging.info(f"Transaction Details: Sender: {transaction['sender']}, "
                 f"Receiver: {transaction['receiver']}, "
                 f"Amount: {transaction['amount']}, "
                 f"Status: {transaction['status']}, "
                 f"Timestamp: {format_timestamp(transaction['timestamp'])}")

def convert_to_dict(transaction):
    """
    Convert a transaction to a dictionary format.
    
    :param transaction: The transaction to convert.
    :return: Dictionary representation of the transaction.
    """
    return {
        'sender': transaction['sender'],
        'receiver': transaction['receiver'],
        'amount': transaction['amount'],
        'contract': transaction.get('contract', None),
        'status': transaction['status'],
        'timestamp': transaction['timestamp']
    }

if __name__ == "__main__":
    # Example usage of utility functions
    sample_transaction = {
        'sender': 'PlanetA',
        'receiver': 'PlanetB',
        'amount': 100,
        'status': 'pending',
        'timestamp': 1633072800  # Example timestamp
    }

    # Log the transaction
    log_transaction(sample_transaction)

    # Validate the transaction data
    is_valid = validate_transaction_data(sample_transaction)
    print(f"Is the transaction valid? {is_valid}")

    # Format the timestamp
    formatted_time = format_timestamp(sample_transaction['timestamp'])
    print(f"Formatted Timestamp: {formatted_time}")

    # Convert to dictionary
    transaction_dict = convert_to_dict(sample_transaction)
    print(f"Transaction Dictionary: {transaction_dict}")
