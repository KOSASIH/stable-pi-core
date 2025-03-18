# integration_example.py

from itp.SRC.interplanetary_transaction_protocol import InterplanetaryTransactionProtocol
from itp.SRC.space_time_synchronization import SpaceTimeSynchronization
import requests  # Example of an external system integration

def fetch_external_data():
    # Simulate fetching data from an external system (e.g., a space agency API)
    response = requests.get("https://api.example.com/celestial_data")
    return response.json()  # Assuming the response is in JSON format

def main():
    # Initialize the components
    itp = InterplanetaryTransactionProtocol()
    stsp = SpaceTimeSynchronization()

    # Fetch external data
    external_data = fetch_external_data()
    print("Fetched External Data:", external_data)

    # Use external data to create a transaction
    transaction = itp.create_transaction(external_data['sender'], external_data['receiver'], external_data['amount'])
    print("Created Transaction from External Data:", transaction)

    # Process the transaction
    itp.process_transactions()
    print("All Transactions:", itp.get_all_transactions())

if __name__ == "__main__":
    main()
