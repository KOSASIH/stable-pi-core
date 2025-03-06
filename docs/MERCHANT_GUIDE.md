# Merchant Guide for Stable Pi Core

Welcome to the Merchant Guide for Stable Pi Core! This document will help you understand how to use the Merchant Tool feature to manage your business transactions using Pi Coin.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Adding a Merchant](#adding-a-merchant)
3. [Managing Items](#managing-items)
4. [Converting Pi Coin to GCV](#converting-pi-coin-to-gcv)
5. [Checking Your Balance](#checking-your-balance)
6. [API Endpoints](#api-endpoints)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

## Getting Started

To begin using the Merchant Tool, you need to have the following:

- A registered account on the Stable Pi Core platform.
- Your wallet address to receive Pi Coin.
- Access to the API endpoints provided by the Stable Pi Core application.

### Prerequisites

- **Node.js**: Ensure you have Node.js installed on your machine.
- **Postman or cURL**: Use Postman or cURL for testing API endpoints.

## Adding a Merchant

To add your merchant profile, you can use the following API endpoint:

### POST `/api/merchants/add`

**Request Body:**

```json
{
    "name": "Your Merchant Name",
    "walletAddress": "YourWalletAddress",
    "items": []
}
```

**Response:**

- **201 Created**: Merchant added successfully.
- **500 Internal Server Error**: If there is an error while adding the merchant.

### Example Request

Using cURL:

```bash
curl -X POST http://localhost:3000/api/merchants/add \
-H "Content-Type: application/json" \
-d '{
    "name": "My Shop",
    "walletAddress": "0xYourWalletAddress",
    "items": []
}'
```

## Managing Items

Once you have added your merchant profile, you can manage your items. To add an item, use the following API endpoint:

### POST `/api/merchants/add-item`

**Request Body:**

```json
{
    "merchantId": "MerchantID",
    "item": {
        "name": "Item Name",
        "priceInPi": 10
    }
}
```

**Response:**

- **201 Created**: Item added successfully.
- **404 Not Found**: If the merchant is not found.
- **500 Internal Server Error**: If there is an error while adding the item.

### Example Request

Using cURL:

```bash
curl -X POST http://localhost:3000/api/merchants/add-item \
-H "Content-Type: application/json" \
-d '{
    "merchantId": "MerchantID",
    "item": {
        "name": "Coffee",
        "priceInPi": 0.5
    }
}'
```

## Converting Pi Coin to GCV

To convert Pi Coin to Global Consensus Value (GCV), use the following API endpoint:

### POST `/api/merchants/convert`

**Request Body:**

```json
{
    "amountInPi": 1,
    "merchantId": "MerchantID"
}
```

**Response:**

- **200 OK**: Returns the equivalent GCV value.
- **404 Not Found**: If the merchant is not found.
- **500 Internal Server Error**: If there is an error during conversion.

### Example Request

Using cURL:

```bash
curl -X POST http://localhost:3000/api/merchants/convert \
-H "Content-Type: application/json" \
-d '{
    "amountInPi": 1,
    "merchantId": "MerchantID"
}'
```

## Checking Your Balance

To check your balance of Pi Coin, use the following API endpoint:

### GET `/api/merchants/balance`

**Query Parameters:**

- `merchantId`: The ID of the merchant.

**Response:**

- **200 OK**: Returns the current balance.
- **404 Not Found**: If the merchant is not found.
- **500 Internal Server Error**: If there is an error while checking the balance.

### Example Request

Using cURL:

```bash
curl -X GET "http://localhost:3000/api/merchants/balance?merchantId=MerchantID"
```

## API Endpoints

Here is a summary of the key API endpoints for merchants:

| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| POST   | `/api/merchants/add `           | Add a new merchant                   |
| POST   | `/api/merchants/add-item`      | Add an item to the merchant's list   |
| POST   | `/api/merchants/convert`       | Convert Pi Coin to GCV               |
| GET    | `/api/merchants/balance`       | Check the merchant's balance          |

## Error Handling

When working with the API, it's essential to handle errors gracefully. Here are some common error responses you might encounter:

- **400 Bad Request**: The request was invalid. Check the request body and parameters.
- **401 Unauthorized**: Authentication failed. Ensure you are using valid credentials.
- **403 Forbidden**: You do not have permission to access this resource.
- **404 Not Found**: The requested resource could not be found.
- **500 Internal Server Error**: An unexpected error occurred on the server.

### Example Error Handling

When making API requests, you should implement error handling in your application. Here’s an example in JavaScript:

```javascript
fetch('http://localhost:3000/api/merchants/add', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: "My Shop",
        walletAddress: "0xYourWalletAddress",
        items: []
    })
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
})
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## Best Practices

To ensure a smooth experience while using the Merchant Tool, consider the following best practices:

- **Keep Your API Keys Secure**: Never expose your API keys in public repositories or client-side code.
- **Validate Input Data**: Always validate the data sent to the API to prevent errors and ensure data integrity.
- **Monitor API Usage**: Keep track of your API usage to avoid hitting rate limits and to optimize performance.
- **Implement Logging**: Use logging to track API requests and responses for debugging and monitoring purposes.

## Conclusion

This guide provides an in-depth overview of how to use the Merchant Tool feature in Stable Pi Core. By following the instructions and examples provided, you can effectively manage your merchant profile, items, and transactions. If you have any questions or need further assistance, please reach out to our support team.

Thank you for being a part of the Stable Pi Core community!
