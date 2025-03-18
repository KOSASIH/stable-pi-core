# transaction_example.py

from itp.SRC.interplanetary_transaction_protocol import InterplanetaryTransactionProtocol

def main():
    # Initialize the Interplanetary Transaction Protocol
    itp = InterplanetaryTransactionProtocol()

    # Create a transaction
    transaction = itp.create_transaction("PlanetA", "PlanetB", 100)
    print("Created Transaction:", transaction)

    # Validate the transaction
    is_valid = itp.validate_transaction(transaction)
    print("Is the Transaction Valid?", is_valid)

    # Execute the transaction
    itp.execute_transaction(transaction)
    print("Executed Transaction:", transaction)

    # Retrieve all transactions
    all_transactions = itp.get_all_transactions()
    print("All Transactions:", all_transactions)

if __name__ == "__main__":
    main()
