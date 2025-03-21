# API Reference for Wormhole Data Bridge (WDB)

## Overview

The Wormhole Data Bridge API provides endpoints for interacting with the blockchain-based stablecoin and governance system. Below is a detailed reference for each available endpoint.

## Base URL

```
http://127.0.0.1:8000
```

## Endpoints

### 1. Mint Tokens

**Endpoint:** `POST /mint`

**Description:** Mints new tokens for a specified recipient.

**Request Body:**
```json
{
    "recipient": "0xRecipientAddress",
    "amount": 1000
}
```

**Response:**
```json
{
    "message": "Tokens minted successfully.",
    "transaction_hash": "0xTransactionHash"
}
```

**Notes:**
- Ensure the recipient address is valid and the amount is a positive integer.

---

### 2. Burn Tokens

**Endpoint:** `POST /burn`

**Description:** Burns a specified amount of tokens from the caller's account.

**Request Body:**
```json
{
    "amount": 500
}
```

**Response:**
```json
{
    "message": "Tokens burned successfully.",
    "transaction_hash": "0xTransactionHash"
}
```

**Notes:**
- The amount must be a positive integer and should not exceed the caller's balance.

---

### 3. Create Proposal

**Endpoint:** `POST /create_proposal`

**Description:** Creates a new governance proposal with a description.

**Request Body:**
```json
{
    "description": "Proposal description here."
}
```

**Response:**
```json
{
    "message": "Proposal created successfully.",
    "transaction_hash": "0xTransactionHash"
}
```

**Notes:**
- The description should provide a clear and concise summary of the proposal.

---

### 4. Vote on Proposal

**Endpoint:** `POST /vote`

**Description:** Casts a vote on a specified proposal.

**Request Body:**
```json
{
    "proposal_id": 1
}
```

**Response:**
```json
{
    "message": "Vote cast successfully.",
    "transaction_hash": "0xTransactionHash"
}
```

**Notes:**
- Ensure the proposal ID is valid and that the voter has not already voted on this proposal.

---

### 5. Execute Proposal

**Endpoint:** `POST /execute_proposal`

**Description:** Executes a specified proposal after it has been approved.

**Request Body:**
```json
{
    "proposal_id": 1
}
```

**Response:**
```json
{
    "message": "Proposal executed successfully.",
    "transaction_hash": "0xTransactionHash"
}
```

**Notes:**
- The proposal must be in a state that allows execution (e.g., approved).

---

### 6. Get Node Location

**Endpoint:** `GET /nodes/{node_id}`

**Description:** Retrieves the location of a specific node in the network.

**Response:**
```json
{
    "node_id": "Node1",
    "location": "LocationA"
}
```

**Notes:**
- Replace `{node_id}` with the actual ID of the node you want to query.

---

### 7. Predict Data Needs

**Endpoint:** `POST /predict/`

**Description:** Predicts future data needs based on provided time points.

**Request Body:**
```json
{
    "future_time": [6, 7, 8]
}
```

**Response:**
```json
{
    "predictions": [350, 400, 450]
}
```

**Notes:**
- The `future_time` array should contain time points for which predictions are needed.

---

### 8. Entangle Data

**Endpoint:** `POST /entangle/`

**Description:** Entangles the provided data.

**Request Body:**
```json
{
    "data": "Hello, Quantum World!"
}
```

**Response:**
```json
{
    "entangled_data": "Entangled(Hello, Quantum World!)"
}
```

**Notes:**
- The data should be a non-empty string to be successfully entangled.

---

## Conclusion

This API reference provides a comprehensive overview of the available endpoints in the Wormhole Data Bridge project. For further assistance, refer to the installation and usage guides, or contact the development team for support.
