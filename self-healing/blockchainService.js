// stable-pi-core/self-healing/blockchainService.js

const Web3 = require('web3');
const { abi: ethereumABI } = require('./EthereumContract.json'); // Replace with your actual ABI file
const { abi: bscABI } = require('./BSCContract.json'); // Replace with your actual ABI file
require('dotenv').config();

// Initialize Web3 instances for Ethereum and BSC
const web3Ethereum = new Web3(new Web3.providers.HttpProvider(process.env.ETHEREUM_RPC_URL));
const web3BSC = new Web3(new Web3.providers.HttpProvider(process.env.BSC_RPC_URL));

// Create contract instances
const ethereumContract = new web3Ethereum.eth.Contract(ethereumABI, process.env.ETHEREUM_CONTRACT_ADDRESS);
const bscContract = new web3BSC.eth.Contract(bscABI, process.env.BSC_CONTRACT_ADDRESS);

/**
 * Interact with the Ethereum contract.
 * @param {string} method - The method name to call on the contract.
 * @param {Array} params - The parameters to pass to the method.
 * @returns {Promise<Object>} - The result of the contract call.
 */
async function interactWithEthereumContract(method, params) {
    const accounts = await web3Ethereum.eth.getAccounts();
    try {
        const result = await ethereumContract.methods[method](...params).send({ from: accounts[0] });
        return result;
    } catch (error) {
        throw new Error(`Ethereum contract interaction failed: ${error.message}`);
    }
}

/**
 * Interact with the BSC contract.
 * @param {string} method - The method name to call on the contract.
 * @param {Array} params - The parameters to pass to the method.
 * @returns {Promise<Object>} - The result of the contract call.
 */
async function interactWithBSCContract(method, params) {
    const accounts = await web3BSC.eth.getAccounts();
    try {
        const result = await bscContract.methods[method](...params).send({ from: accounts[0] });
        return result;
    } catch (error) {
        throw new Error(`BSC contract interaction failed: ${error.message}`);
    }
}

/**
 * Fetch the current account balance of a given address on Ethereum.
 * @param {string} address - The Ethereum address to check.
 * @returns {Promise<string>} - The balance in Ether.
 */
async function getEthereumBalance(address) {
    try {
        const balanceWei = await web3Ethereum.eth.getBalance(address);
        return web3Ethereum.utils.fromWei(balanceWei, 'ether');
    } catch (error) {
        throw new Error(`Failed to fetch Ethereum balance: ${error.message}`);
    }
}

/**
 * Fetch the current account balance of a given address on BSC.
 * @param {string} address - The BSC address to check.
 * @returns {Promise<string>} - The balance in BNB.
 */
async function getBSCBalance(address) {
    try {
        const balanceWei = await web3BSC.eth.getBalance(address);
        return web3BSC.utils.fromWei(balanceWei, 'ether'); // BSC uses the same unit as Ether
    } catch (error) {
        throw new Error(`Failed to fetch BSC balance: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    interactWithEthereumContract,
    interactWithBSCContract,
    getEthereumBalance,
    getBSCBalance
};
