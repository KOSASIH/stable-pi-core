# Dual Value System User Guide for Stable Pi Core

Welcome to the Dual Value System User Guide for Stable Pi Core! This document will help you understand how to use the Dual Value System feature, which allows users to benefit from both a stable value and a market-driven value for Pi Coin.

## Table of Contents

1. [Understanding the Dual Value System](#understanding-the-dual-value-system)
2. [Getting Started](#getting-started)
3. [Using the Dual Value System](#using-the-dual-value-system)
4. [API Endpoints](#api-endpoints)
5. [Example Use Cases](#example-use-cases)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Conclusion](#conclusion)

## Understanding the Dual Value System

The Dual Value System allows Pi Coin to maintain two distinct values:

- **Stable Value**: This is a fixed value that Pi Coin is pegged to, ensuring stability in transactions and holdings.
- **Market-Driven Value**: This value fluctuates based on market conditions, allowing users to take advantage of price movements.

This system provides flexibility for users, enabling them to choose between stability and potential growth.

## Getting Started

To begin using the Dual Value System, you need to have the following:

- A registered account on the Stable Pi Core platform.
- Access to the API endpoints provided by the Stable Pi Core application.

## Using the Dual Value System

### Converting Between Values

You can convert between the stable value and the market-driven value using the following API endpoint:

### POST `/api/dual-value/convert`

**Request Body:**

```json
{
    "amount": 10,
    "fromValueType": "stable", // or "market"
    "toValueType": "market" // or "stable"
}
```

**Response:**

- **200 OK**: Returns the converted amount.
- **400 Bad Request**: If the request is invalid.
- **500 Internal Server Error**: If there is an error during conversion.

### Example Request

Using cURL:

```bash
curl -X POST http://localhost:3000/api/dual-value/convert \
-H "Content-Type: application/json" \
-d '{
    "amount": 10,
    "fromValueType": "stable",
    "toValueType": "market"
}'
```

## API Endpoints

Here is a summary of the key API endpoints for the Dual Value System:

| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| POST   | `/api/dual-value/convert`      | Convert between stable and market-driven values |

## Example Use Cases

### Use Case 1: Converting Stable Value to Market Value

If you have 10 Pi Coins at a stable value and want to convert them to their market-driven equivalent, you would send a request to the `/convert` endpoint as shown above.

### Use Case 2: Converting Market Value to Stable Value

If you have 5 Pi Coins at the market-driven value and want to convert them to the stable value, you would adjust the request accordingly:

```json
{
    "amount": 5,
    "fromValueType": "market",
    "toValueType": "stable"
}
```

## Error Handling

When working with the API, it's essential to handle errors gracefully. Here are some common error responses you might encounter:

- **400 Bad Request**: The request was invalid. Check the request body and parameters.
- **404 Not Found**: The requested resource could not be found.
- **500 Internal Server Error**: An unexpected error occurred on the server.

### Example Error Handling

When making API requests, you should implement error handling in your application. Here’s an example in JavaScript:

```javascript
fetch('http://localhost:3000/api/dual-value/convert', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        amount: 10,
        fromValueType: "stable",
        toValueType: "market"
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

To ensure a smooth experience while using the Dual Value System, consider the following best practices:

- **Keep Your API Keys Secure**: Never expose your API keys in public repositories or client-side code.
- **Validate Input Data**: Always validate the data sent to the API to prevent errors and ensure data integrity.
- **Monitor API Usage**: Keep track of your API usage to avoid hitting rate limits and to optimize performance.
- **Implement Logging**: Use logging to track API requests and responses for debugging and monitoring purposes.

## Conclusion

This guide provides an in-depth overview of how to use the Dual Value System feature in Stable Pi Core. By following the instructions and examples provided, you can effectively manage your transactions and take advantage of both stable and market-driven values for Pi Coin. If you have any questions or need further assistance, please reach out to our support team.

Thank you for being a part of the Stable Pi Core community!
