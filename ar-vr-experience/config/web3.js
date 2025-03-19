// ar-vr-experience/config/web3.js

const Web3 = require('web3');
const dotenv = require('dotenv');
const winston = require('winston'); // For logging

dotenv.config();

// Logger configuration
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'web3.log' })
    ],
});

// Define the supported networks
const NETWORKS = {
    ETHEREUM: process.env.ETHEREUM_API_URL || 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID',
    ROPSTEN: process.env.ROPSTEN_API_URL || 'https://ropsten.infura.io/v3/YOUR_INFURA_PROJECT_ID',
    BSC: process.env.BSC_API_URL || 'https://bsc-dataseed.binance.org/',
    POLYGON: process.env.POLYGON_API_URL || 'https://polygon-rpc.com/',
    // Add more networks as needed
};

// Initialize Web3 instance
let web3 = new Web3(new Web3.providers.HttpProvider(NETWORKS.ETHEREUM)); // Default to Ethereum mainnet

// Function to set the network
const setNetwork = (network) => {
    if (NETWORKS[network]) {
        web3.setProvider(new Web3.providers.HttpProvider(NETWORKS[network]));
        logger.info(`Web3 provider set to ${network}`);
    } else {
        logger.error(`Network ${network} is not supported.`);
        throw new Error(`Network ${network} is not supported.`);
    }
};

// Function to get the current network
const getCurrentNetwork = () => {
    return web3.currentProvider.host;
};

// Custom error class for Web3 errors
class Web3Error extends Error {
    constructor(message) {
        super(message);
        this.name = 'Web3Error';
    }
}

// Function to interact with a smart contract
const interactWithContract = async (contractAddress, abi, methodName, params, fromAddress, privateKey) => {
    const contract = new web3.eth.Contract(abi, contractAddress);
    try {
        const data = contract.methods[methodName](...params).encodeABI();
        const nonce = await web3.eth.getTransactionCount(fromAddress);
        const gasPrice = await web3.eth.getGasPrice();
        const gasLimit = await contract.methods[methodName](...params).estimateGas({ from: fromAddress });

        const tx = {
            from: fromAddress,
            to: contractAddress,
            data,
            gas: gasLimit,
            gasPrice,
            nonce,
        };

        const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);
        const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
        logger.info(`Transaction successful: ${receipt.transactionHash}`);
        return receipt;
    } catch (error) {
        logger.error('Error interacting with contract:', error);
        throw new Web3Error('Failed to interact with contract');
    }
};

// Function to deploy a smart contract
const deployContract = async (abi, bytecode, fromAddress, privateKey, constructorArgs = []) => {
    const contract = new web3.eth.Contract(abi);
    try {
        const nonce = await web3.eth.getTransactionCount(fromAddress);
        const gasPrice = await web3.eth.getGasPrice();
        const gasLimit = await contract.deploy({ data: bytecode, arguments: constructorArgs }).estimateGas();

        const tx = {
            from: fromAddress,
            gas: gasLimit,
            gasPrice,
            data: contract.deploy({ data: bytecode, arguments: constructorArgs }).encodeABI(),
            nonce,
        };

        const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);
        const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
        logger.info(`Contract deployed successfully: ${receipt.contractAddress}`);
        return receipt.contractAddress;
    } catch (error) {
        logger.error('Error deploying contract:', error);
        throw new Web3Error('Failed to deploy contract');
    }
};

// Function to listen for events from a smart contract
const listenToEvents = (contractAddress, abi, eventName, callback, filter = {}) => {
    const contract = new web3.eth.Contract(abi, contractAddress);
    contract.events[eventName](filter)
        .on('data', (event) => {
            logger.info(`Event ${eventName} received:`, event);
            callback(event);
        })
        .on('error', (error) => {
            logger.error('Error listening to events:', error);
        });
};

// Function to manage transactions with retries
const sendTransactionWithRetry = async (tx, retries = 3) => {
    try {
        const receipt = await web3.eth.sendTransaction(tx);
        logger.info(`Transaction successful: ${receipt.transactionHash}`);
        return receipt;
    } catch (error) {
        if (retries > 0) {
            logger.warn(`Transaction failed, retrying... (${retries} retries left)`);
            return sendTransactionWithRetry(tx, retries - 1);
        } else {
            logger.error('Transaction failed after retries:', error);
            throw new Web3Error('Transaction failed after retries');
        }
    }
};

// Utility function to convert Ether to Wei
const toWei = (amount) => {
    return web3.utils.toWei(amount.toString(), 'ether');
};

// Utility function to convert Wei to Ether
const fromWei = (amount) => {
    return web3.utils.fromWei(amount.toString(), 'ether');
};

// Utility function to validate Ethereum addresses
const isValidAddress = (address) => {
    return web3.utils.isAddress(address);
};

// Export the Web3 instance and utility functions
module.exports = {
    web3,
    setNetwork,
    getCurrentNetwork,
    interactWithContract,
    deployContract,
    listenToEvents,
    sendTransactionWithRetry,
    toWei,
    fromWei,
    isValidAddress,
};
