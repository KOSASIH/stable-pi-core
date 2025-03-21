# Usage Guide for Wormhole Data Bridge (WDB)

## Accessing the API

Once the API is running, you can access it at `http://127.0.0.1:8000`. You can use tools like Postman, curl, or any HTTP client to interact with the API.

## API Endpoints

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

**Example Request using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/mint" -H "Content-Type: application/json" -d '{"recipient": "0xRecipientAddress", "amount": 1000}'
```

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

**Example Request using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/burn" -H "Content-Type: application/json" -d '{"amount": 500}'
```

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

**Example Request using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/create_proposal" -H "Content-Type: application/json" -d '{"description": "Proposal description here."}'
```

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

**Example Request using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/vote" -H "Content-Type: application/json" -d '{"proposal_id": 1}'
```

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

**Example Request using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/execute_proposal" -H "Content-Type: application/json" -d '{"proposal_id": 1}'
```

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

**Example Request using curl:**
```bash
curl -X GET "http://127.0.0.1:8000/nodes/Node1"
```

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

**Example Request using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/predict/" -H "Content-Type: application/json" -d '{"future_time": [6, 7, 8]}'
```

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

**Example Request using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/entangle/" -H "Content-Type: application/json" -d '{"data": "Hello, Quantum World!"}'
```

## Conclusion

You can now interact with the Wormhole Data Bridge API using the provided endpoints. Make sure to replace placeholder values (like addresses and proposal IDs) with actual data when making requests. For further assistance, refer to the API reference or installation guide.
