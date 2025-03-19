"""
Interplanetary Transaction Protocol (ITP) Package

This package implements the Interplanetary Transaction Protocol (ITP),
which facilitates secure and efficient transactions across celestial bodies
using advanced synchronization and consensus mechanisms.

Key Features:
- **Transaction Management**: Create, validate, and execute transactions between celestial entities.
- **Space-Time Synchronization**: Ensure accurate timekeeping across different celestial bodies.
- **Quantum Entanglement Consensus**: Utilize quantum mechanics for secure and rapid consensus on transactions.

Modules:
- `interplanetary_transaction_protocol`: Core implementation of the ITP.
- `space_time_synchronization`: Handles time synchronization across celestial bodies.
- `quantum_entanglement_consensus`: Implements consensus mechanisms based on quantum entanglement.
- `transaction_manager`: Manages the lifecycle of transactions, including validation and execution.
- `utils`: Provides utility functions for various operations within the ITP.

Usage:
To use the ITP package, import the necessary classes and create instances as needed. For example:

```python
from itp.SRC import InterplanetaryTransactionProtocol

itp = InterplanetaryTransactionProtocol()
transaction = itp.create_transaction("PlanetA", "PlanetB", 100)
itp.process_transactions()
