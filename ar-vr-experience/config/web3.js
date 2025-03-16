// ar-vr-experience/config/web3.js

const Web3 = require('web3');
const dotenv = require('dotenv');

dotenv.config();

// Define the supported networks
const NETWORKS = {
    ETHEREUM: process.env.ETHEREUM_API_URL || 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID', // Replace with your Infura project ID
    ROPSTEN: process.env.ROPSTEN_API_URL || 'https://ropsten.infura.io/v3/YOUR_INFURA_PROJECT_ID', // Replace with your Infura project ID
    BSC: process.env.BSC_API_URL || 'https://bsc-dataseed.binance.org/', // Binance Smart Chain
    // Add more networks as needed
};

// Initialize Web3 instance
let web3 = new Web3(new Web3.providers.HttpProvider(NETWORKS.ETHEREUM)); // Default to Ethereum mainnet

// Function to set the network
const setNetwork = (network) => {
    if (NETWORKS[network]) {
        web3.setProvider(new Web3.providers.HttpProvider(NETWORKS[network]));
        console.log(`Web3 provider set to ${network}`);
    } else {
        throw new Error(`Network ${network} is not supported.`);
    }
};

// Function to get the current network
const getCurrentNetwork = () => {
    return web3.currentProvider.host;
};

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
        return receipt;
    } catch (error) {
        console.error('Error interacting with contract:', error);
        throw new Error('Failed to interact with contract');
    }
};

// Function to listen for events from a smart contract
const listenToEvents = (contractAddress, abi, eventName, callback) => {
    const contract = new web3.eth.Contract(abi, contractAddress);
    contract.events[eventName]()
        .on('data', (event) => {
            console.log(`Event ${eventName} received:`, event);
            callback(event);
        })
        .on('error', (error) => {
            console.error('Error listening to events:', error);
        });
};

// Utility function to convert Ether to Wei
const toWei = (amount) => {
    return web3.utils.toWei(amount.toString(), 'ether');
};

// Utility function to convert Wei to Ether
const fromWei = (amount) => {
    return web3.utils.fromWei(amount.toString(), 'ether');
};

// Export the Web3 instance and utility functions
module.exports = {
    web3,
    setNetwork,
    getCurrentNetwork,
    interactWithContract,
    listenToEvents,
    toWei,
    fromWei,
};
