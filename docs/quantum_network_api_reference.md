# API Reference for Stable Pi Core

Welcome to the API reference for the Stable Pi Core project. This document provides detailed information about the available APIs for interacting with the quantum network and blockchain components.

## Table of Contents

- [Quantum Network API](#quantum-network-api)
  - [Node Management](#node-management)
  - [Quantum Communication](#quantum-communication)
  - [Quantum Key Distribution (QKD)](#quantum-key-distribution-qkd)
  - [Quantum Oracle](#quantum-oracle)
- [Blockchain API](#blockchain-api)
  - [Smart Contracts](#smart-contracts)
  - [Blockchain Interface](#blockchain-interface)

---

## Quantum Network API

### Node Management

#### Create Node

- **Endpoint**: `POST /api/quantum/nodes`
- **Description**: Creates a new quantum node in the network.
- **Parameters**:
  - `name` (string, required): The name of the node.
  - `location` (string, optional): The physical location of the node.
- **Response**:
  - `201 Created`: Returns the created node object.
  - `400 Bad Request`: If the input parameters are invalid.

#### Get Node

- **Endpoint**: `GET /api/quantum/nodes/{node_id}`
- **Description**: Retrieves information about a specific quantum node.
- **Parameters**:
  - `node_id` (string, required): The unique identifier of the node.
- **Response**:
  - `200 OK`: Returns the node object.
  - `404 Not Found`: If the node does not exist.

### Quantum Communication

#### Send Quantum Message

- **Endpoint**: `POST /api/quantum/communication/send`
- **Description**: Sends a quantum message between nodes.
- **Parameters**:
  - `sender_id` (string, required): The ID of the sender node.
  - `receiver_id` (string, required): The ID of the receiver node.
  - `message` (string, required): The quantum message to be sent.
- **Response**:
  - `200 OK`: Returns a confirmation of the message sent.
  - `400 Bad Request`: If the parameters are invalid.

### Quantum Key Distribution (QKD)

#### Initiate QKD Session

- **Endpoint**: `POST /api/quantum/qkd/initiate`
- **Description**: Initiates a Quantum Key Distribution session between two nodes.
- **Parameters**:
  - `node_a_id` (string, required): The ID of the first node.
  - `node_b_id` (string, required): The ID of the second node.
- **Response**:
  - `200 OK`: Returns session details.
  - `400 Bad Request`: If the parameters are invalid.

### Quantum Oracle

#### Query Oracle

- **Endpoint**: `POST /api/quantum/oracle/query`
- **Description**: Queries the quantum oracle for specific information.
- **Parameters**:
  - `query` (string, required): The query string to be processed by the oracle.
- **Response**:
  - `200 OK`: Returns the result of the query.
  - `500 Internal Server Error`: If the oracle fails to process the query.

---

## Blockchain API

### Smart Contracts

#### Deploy Smart Contract

- **Endpoint**: `POST /api/blockchain/smart_contracts/deploy`
- **Description**: Deploys a new smart contract to the blockchain.
- **Parameters**:
  - `contract_code` (string, required): The code of the smart contract.
  - `initial_parameters` (object, optional): Initial parameters for the contract.
- **Response**:
  - `201 Created`: Returns the deployed contract address.
  - `400 Bad Request`: If the contract code is invalid.

#### Execute Smart Contract

- **Endpoint**: `POST /api/blockchain/smart_contracts/execute`
- **Description**: Executes a function of a deployed smart contract.
- **Parameters**:
  - `contract_address` (string, required): The address of the smart contract.
  - `function_name` (string, required): The name of the function to execute.
  - `args` (array, optional): Arguments for the function.
- **Response**:
  - `200 OK`: Returns the result of the function execution.
  - `404 Not Found`: If the contract does not exist.

### Blockchain Interface

#### Get Blockchain Status

- **Endpoint**: `GET /api/blockchain/status`
- **Description**: Retrieves the current status of the blockchain.
- **Response**:
  - `200 OK`: Returns the current status of the blockchain, including block height and network health.
  - `500 Internal Server Error`: If there is an issue retrieving the status.

#### Get Transaction Details

- **Endpoint**: `GET /api/blockchain/transactions/{transaction_id}`
- **Description**: Retrieves details of a specific transaction.
- **Parameters**:
  - `transaction_id` (string, required): The unique identifier of the transaction.
- **Response**:
  - `200 OK`: Returns the transaction details.
  - `404 Not Found`: If the transaction does not exist.

---

## Error Handling

All API responses will include an error message in the following format when applicable:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Detailed error message."
  }
}
```

## Authentication

All API endpoints require authentication via an API key. Include the API key in the request header as follows:

```
Authorization: Bearer YOUR_API_KEY
```

## Rate Limiting

To ensure fair usage, the API enforces rate limits. Exceeding the limit will result in a `429 Too Many Requests` response.

---

## Conclusion

This API reference provides a comprehensive overview of the functionalities available in the Stable Pi Core project. For further assistance, please refer to the documentation or contact the development team.
