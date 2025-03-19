# example_usage.py

from itp.SRC.interplanetary_transaction_protocol import InterplanetaryTransactionProtocol
from itp.SRC.space_time_synchronization import SpaceTimeSynchronization
from itp.SRC.quantum_entanglement_consensus import QuantumEntanglementConsensus

def main():
    # Initialize the components
    itp = InterplanetaryTransactionProtocol()
    stsp = SpaceTimeSynchronization()
    qgc = QuantumEntanglementConsensus()

    # Synchronize time with a celestial body (simulated)
    celestial_time = 1633072800  # Example celestial body time
    stsp.synchronize_time(celestial_time)

    # Create a transaction
    transaction = itp.create_transaction("PlanetA", "PlanetB", 100)
    print("Created Transaction:", transaction)

    # Process the transaction
    itp.process_transactions()
    print("All Transactions:", itp.get_all_transactions())

    # Propose the transaction to the consensus mechanism
    qgc.propose_transaction(transaction)
    validated_transactions = qgc.reach_consensus()
    print("Validated Transactions:", validated_transactions)

if __name__ == "__main__":
    main()
