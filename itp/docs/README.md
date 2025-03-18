## Interplanetary Transaction Protocol (ITP)

### Description
The Interplanetary Transaction Protocol (ITP) is a specialized protocol designed to facilitate secure and efficient transactions across celestial bodies. It leverages advanced technologies to ensure that transactions are processed reliably, even in the vastness of space where traditional methods may fail.

### Key Features
- **Cross-Planetary Payments**: ITP enables seamless transactions between different planets, moons, or other celestial entities, allowing for a new era of interplanetary commerce.
- **Space-Time Synchronization**: By integrating the Space-Time Synchronization Protocol (STSP), ITP ensures that all transactions are timestamped accurately, accounting for the time differences and communication delays that occur across vast distances in space.
- **Quantum Entanglement-Based Consensus**: The protocol employs Quantum Entanglement-Based Consensus (QGC) to achieve rapid and secure agreement on transaction validity among distributed nodes. This consensus mechanism utilizes principles of quantum mechanics to enhance security and efficiency, making it suitable for the unique challenges of interplanetary transactions.

### How It Works
1. **Transaction Creation**: Users can create transactions specifying the sender, receiver, and amount. Each transaction is assigned a unique timestamp using the synchronized time provided by the STSP.
2. **Validation**: Before execution, transactions are validated to ensure they meet predefined criteria (e.g., positive amounts, valid sender and receiver).
3. **Consensus**: Validated transactions are proposed to the consensus mechanism, where nodes reach agreement on their validity using quantum entanglement principles.
4. **Execution**: Once consensus is reached, transactions are executed, and the results are recorded. Smart contracts can also be executed as part of the transaction process, allowing for automated and conditional transactions.

### Use Cases
- **Interplanetary Trade**: Facilitate trade between colonies on different planets, enabling the exchange of goods and services.
- **Resource Management**: Manage and allocate resources across celestial bodies, ensuring fair and efficient distribution.
- **Scientific Collaboration**: Support collaborative projects between research teams on different planets, allowing for shared funding and resource allocation.

### Example Usage
```python
from itp.SRC.interplanetary_transaction_protocol import InterplanetaryTransactionProtocol

# Initialize the Interplanetary Transaction Protocol
itp = InterplanetaryTransactionProtocol()

# Create a transaction
transaction = itp.create_transaction("PlanetA", "PlanetB", 100)

# Process transactions
itp.process_transactions()

# Print all transactions
print(itp.get_all_transactions())
