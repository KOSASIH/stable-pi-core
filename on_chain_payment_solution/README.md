# On-Chain Payment Solution

## Overview

The On-Chain Payment Solution is a decentralized application (DApp) that allows users to make and manage payments using various cryptocurrencies and fiat currencies. Built on Ethereum, this solution leverages smart contracts for secure payment processing and refund management. The DApp provides a user-friendly interface for interacting with the blockchain, making it easy for users to create payments, request refunds, and view transaction history.

## Features

- **Payment Processing**: Users can create payments in multiple currencies (fiat and cryptocurrencies).
- **Refund Management**: Users can request refunds for their payments, which can be processed by the contract owner.
- **Transaction History**: Users can view their transaction history within the DApp.
- **Wallet Integration**: Seamless integration with popular Ethereum wallets like MetaMask.
- **Responsive Design**: The DApp is designed to work on both desktop and mobile devices.

## Technologies Used

- **Solidity**: Smart contracts for payment processing and refund management.
- **React**: Frontend framework for building the DApp.
- **Web3.js**: Library for interacting with the Ethereum blockchain.
- **Truffle**: Development framework for Ethereum smart contracts.
- **OpenZeppelin**: Library for secure smart contract development.

## Installation

### Prerequisites

- Node.js (v14 or later)
- npm (Node Package Manager)
- Truffle (v5 or later)
- Ganache (for local blockchain development)

### Clone the Repository

```bash
git clone https://github.com/KOSASIH/stable-pi-core.git
cd stable-pi-core/on_chain_payment_solution
```

### Install Dependencies

1. **Backend (Smart Contracts)**

   Navigate to the `contracts` directory and install dependencies:

   ```bash
   cd contracts
   npm install
   ```

2. **Frontend (DApp)**

   Navigate to the `dapp` directory and install dependencies:

   ```bash
   cd dapp
   npm install
   ```

### Compile and Migrate Smart Contracts

1. Start Ganache to create a local Ethereum blockchain.
2. In the `contracts` directory, compile the smart contracts:

   ```bash
   truffle compile
   ```

3. Migrate the smart contracts to the local blockchain:

   ```bash
   truffle migrate --network development
   ```

## Running the DApp

1. Navigate to the `dapp` directory:

   ```bash
   cd dapp
   ```

2. Start the development server:

   ```bash
   npm start
   ```

3. Open your browser and go to `http://localhost:3000` to access the DApp.

## Usage

1. **Connect Wallet**: Click the "Connect Wallet" button to connect your Ethereum wallet (e.g., MetaMask).
2. **Create Payment**: Fill in the payment form with the amount and currency, then submit to create a payment.
3. **View Transaction History**: Check the transaction history section to see your past payments.
4. **Request Refund**: If applicable, you can request a refund for any pending payments.

## Testing

To run the unit tests for the smart contracts, navigate to the `contracts` directory and execute:

```bash
truffle test
```

To run the integration tests for the DApp, navigate to the `tests` directory and execute:

```bash
npm test
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenZeppelin](https://openzeppelin.com/) for their secure smart contract libraries.
- [React](https://reactjs.org/) for building the user interface.
- [Truffle](https://www.trufflesuite.com/truffle) for smart contract development and testing.
- [Ganache](https://www.trufflesuite.com/ganache) for local blockchain development.
