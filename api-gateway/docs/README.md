# Stable-Pi-Core API Gateway

The Stable-Pi-Core API Gateway is a modular and extensible API gateway designed to facilitate interactions with various blockchains, including Ethereum and Bitcoin. It provides a unified interface for fetching blockchain data, sending transactions, and querying prices.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [GraphQL API](#graphql-api)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Modular Architecture**: Easily extendable to support additional blockchains and services.
- **RESTful and GraphQL APIs**: Provides both RESTful endpoints and a GraphQL interface for flexible data retrieval.
- **Authentication**: Supports JWT-based authentication for secure access to protected routes.
- **Logging and Error Handling**: Centralized logging and error handling for better monitoring and debugging.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd stable-pi-core
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Set up environment variables**: Create a `.env` file in the root directory and add the following variables:

   ```plaintext
   PORT=4000
   ETHEREUM_API_URL=https://api.etherscan.io/api
   BITCOIN_API_URL=https://api.blockcypher.com/v1/btc/main
   JWT_SECRET=your_jwt_secret
   ```

4. **Start the server**:

   ```bash
   npm start
   ```

   The API Gateway will be running at `http://localhost:4000`.

## Usage

### RESTful API Endpoints

- **Ethereum Endpoints**:
  - `GET /api/ethereum/block/:blockNumber`: Fetch Ethereum block data by block number.
  - `GET /api/ethereum/transaction/:transactionHash`: Fetch Ethereum transaction data by transaction hash.
  - `POST /api/ethereum/contract/:contractAddress/call`: Call a method on a smart contract (requires authentication).

- **Bitcoin Endpoints**:
  - `GET /api/bitcoin/block/:blockHeight`: Fetch Bitcoin block data by block height.
  - `GET /api/bitcoin/transaction/:transactionHash`: Fetch Bitcoin transaction data by transaction hash.
  - `POST /api/bitcoin/send`: Send a Bitcoin transaction (requires authentication).
  - `GET /api/bitcoin/price`: Fetch the current Bitcoin price.

### GraphQL API

The GraphQL API is available at `http://localhost:4000/graphql`. You can use the following queries:

- **Ethereum Queries**:
  ```graphql
  query {
      ethereumBlock(blockNumber: "0x10d4e") {
          number
          hash
          transactions {
              hash
              from
              to
              value
          }
      }
      ethereumTransaction(transactionHash: "0x5c69b...") {
          hash
          from
          to
          value
      }
  }
  ```

- **Bitcoin Queries**:
  ```graphql
  query {
      bitcoinBlock(blockHeight: "100000") {
          number
          hash
          transactions {
              hash
              from
              to
              value
          }
      }
      bitcoinTransaction(transactionHash: "0x5c69b...") {
          hash
          from
          to
          value
      }
      bitcoinPrice
  }
  ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Create a pull request describing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
