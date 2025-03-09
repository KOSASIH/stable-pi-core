# Token Incentive System

A super advanced decentralized application (dApp) that implements a token incentive system with staking mechanisms. This project allows users to stake tokens, earn rewards, and interact with the Ethereum blockchain.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Token Creation**: Create and manage an ERC20 token.
- **Staking Mechanism**: Users can stake their tokens to earn rewards.
- **Dynamic Reward Rates**: The owner can adjust the reward rates for staking.
- **API Integration**: RESTful API for interacting with the staking system.
- **MongoDB Integration**: Store user data and contributions in a MongoDB database.
- **Security**: Utilizes OpenZeppelin contracts for secure token and staking implementations.

## Technologies Used

- **Ethereum**: Smart contracts written in Solidity.
- **Node.js**: Backend server using Express.
- **MongoDB**: Database for storing user data.
- **Web3.js**: Library for interacting with the Ethereum blockchain.
- **Hardhat**: Development environment for Ethereum.
- **Mongoose**: ODM for MongoDB.
- **Jest/Mocha**: Testing frameworks for unit and integration tests.

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- MongoDB (local or cloud instance)
- An Ethereum wallet (e.g., MetaMask) for testing
- Infura or Alchemy account for Ethereum node access (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd stable-pi-core/token-incentive-system
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory and add your environment variables:

   ```plaintext
   MONGODB_URI=mongodb://<username>:<password>@localhost:27017/mydatabase
   INFURA_URL=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
   PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
   PORT=5000
   NODE_ENV=development
   REWARD_TOKEN_ADDRESS=0xYOUR_REWARD_TOKEN_CONTRACT_ADDRESS
   STAKING_CONTRACT_ADDRESS=0xYOUR_STAKING_CONTRACT_ADDRESS
   ```

4. Start the MongoDB server (if using a local instance):

   ```bash
   mongod
   ```

## Usage

### Running the Application

To start the application in development mode, use:

```bash
npm run dev
```

This will start the Express server and watch for changes.

### Running Tests

To run the unit tests for the smart contracts and API endpoints, use:

```bash
npm test
```

## API Documentation

### Base URL

```
http://localhost:5000
```

### Endpoints

- **GET /**: Check if the API is running.
  - **Response**: `{"message": "API is running..."}`

- **POST /stake**: Stake tokens.
  - **Request Body**:
    ```json
    {
      "user": "0xAddress",
      "amount": "50"
    }
    ```
  - **Response**: `{"message": "Tokens staked successfully"}`

- **POST /unstake**: Unstake tokens and claim rewards.
  - **Request Body**:
    ```json
    {
      "user": "0xAddress"
    }
    ```
  - **Response**: `{"message": "Tokens unstaked successfully"}`

- **GET /users**: Get user information.
  - **Response**: Returns user data including staking balance and rewards.

## Deployment

To deploy the smart contracts, use:

```bash
npx hardhat run scripts/deploy.js --network <network_name>
```

Replace `<network_name>` with the desired Ethereum network ( e.g., `rinkeby` or `mainnet`).

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenZeppelin](https://openzeppelin.com/) for their secure smart contract libraries.
- [Hardhat](https://hardhat.org/) for the Ethereum development environment.
- [MongoDB](https://www.mongodb.com/) for the database solution.
- [Express](https://expressjs.com/) for the web framework.
- [Web3.js](https://web3js.readthedocs.io/) for Ethereum blockchain interaction.
- [Mongoose](https://mongoosejs.com/) for MongoDB object modeling.
