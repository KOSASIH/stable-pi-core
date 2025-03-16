# User Guide for Quantum Network Features

## Introduction

This user guide provides instructions on how to utilize the features of the Quantum Network. It covers the setup process, how to interact with quantum nodes, send and receive messages, and utilize the blockchain integration for secure transactions.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Interacting with Quantum Nodes](#interacting-with-quantum-nodes)
4. [Sending and Receiving Messages](#sending-and-receiving-messages)
5. [Using the Quantum Oracle](#using-the-quantum-oracle)
6. [Blockchain Integration](#blockchain-integration)
7. [Troubleshooting](#troubleshooting)
8. [Conclusion](#conclusion)

## Prerequisites

Before using the Quantum Network, ensure you have the following:

- Python 3.7 or higher
- Required Python packages (install via `requirements.txt`)
- Access to an Ethereum node (e.g., Infura)
- A deployed smart contract on the Ethereum network

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd stable-pi-core
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Ethereum credentials:
   ```plaintext
   INFURA_URL=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
   PRIVATE_KEY=YOUR_PRIVATE_KEY
   ACCOUNT_ADDRESS=0xYourAccountAddress
   ```

## Interacting with Quantum Nodes

### Creating a Quantum Node

To create a new quantum node, use the following command in your Python script:

```python
from quantum_network.node import QuantumNode

# Create a new quantum node
node = QuantumNode(node_id="node_1", qubit_state="0b0")
```

### Updating Qubit State

You can update the qubit state of a node as follows:

```python
node.update_qubit_state("0b1")
```

## Sending and Receiving Messages

### Sending a Message

To send a message using quantum communication, use the `QuantumCommunication` class:

```python
from quantum_network.communication import QuantumCommunication

communication = QuantumCommunication()
success = communication.send_message("Hello, Quantum World!")
if success:
    print("Message sent successfully!")
```

### Receiving a Message

To receive a message, call the `receive_message` method:

```python
message = communication.receive_message()
print(f"Received message: {message}")
```

## Using the Quantum Oracle

### Querying the Oracle

To query the quantum oracle, use the following code:

```python
from quantum_network.oracle import QuantumOracle

oracle = QuantumOracle()
result = oracle.query("What is the state of the qubit?")
print(f"Oracle response: {result}")
```

## Blockchain Integration

### Sending a Transaction

To send a transaction to the smart contract, use the `BlockchainInterface` class:

```python
from blockchain.blockchain_interface import BlockchainInterface

blockchain_interface = BlockchainInterface(INFURA_URL, CONTRACT_ADDRESS, CONTRACT_ABI, PRIVATE_KEY, ACCOUNT_ADDRESS)
txn_hash = blockchain_interface.send_transaction('storeQuantumData', {'qubit_state': '0b1010', 'metadata': 'Quantum data'})
print(f'Transaction sent with hash: {txn_hash}')
```

### Checking Account Balance

To check your Ethereum account balance:

```python
balance = blockchain_interface.get_balance()
print(f'Account balance: {balance} ETH')
```

### Calling Smart Contract Functions

To call a read-only function from the smart contract:

```python
quantum_data = blockchain_interface.call_contract_function('getQuantumData', 1)
print(f'Retrieved quantum data: {quantum_data}')
```

## Troubleshooting

- **Connection Issues**: Ensure your Infura URL is correct and that you have an active internet connection.
- **Transaction Failures**: Check your Ethereum account balance and ensure you have enough gas to cover transaction fees.
- **Smart Contract Errors**: Verify that the smart contract is deployed correctly and that you are using the correct ABI and address.

## Conclusion

This user guide provides a comprehensive overview of how to utilize the features of the Quantum Network. For further assistance, please refer to the documentation or contact the support team.
