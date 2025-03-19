// helpers.js
require('dotenv').config();
const { ethers } = require('hardhat');

/**
 * Deploys a new contract using the provided contract name and constructor arguments.
 * @param {string} contractName - The name of the contract to deploy.
 * @param {Array} args - The constructor arguments for the contract.
 * @param {Object} signer - The signer to deploy the contract with.
 * @returns {Promise<Contract>} - The deployed contract instance.
 */
async function deployContract(contractName, args = [], signer) {
    const ContractFactory = await ethers.getContractFactory(contractName, signer);
    const contract = await ContractFactory.deploy(...args);
    await contract.deployed();
    console.log(`${contractName} deployed at: ${contract.address}`);
    return contract;
}

/**
 * Sends a transaction to a specified contract method.
 * @param {Contract} contract - The contract instance to interact with.
 * @param {string} methodName - The name of the method to call.
 * @param {Array} params - The parameters to pass to the method.
 * @param {Object} signer - The signer to send the transaction with.
 * @returns {Promise<TransactionResponse>} - The transaction response.
 */
async function sendTransaction(contract, methodName, params = [], signer) {
    const tx = await contract.connect(signer)[methodName](...params);
    console.log(`Transaction sent: ${tx.hash}`);
    await tx.wait();
    console.log(`Transaction confirmed: ${tx.hash}`);
    return tx;
}

/**
 * Queries a contract's state for a specific method.
 * @param {Contract} contract - The contract instance to interact with.
 * @param {string} methodName - The name of the method to call.
 * @param {Array} params - The parameters to pass to the method.
 * @returns {Promise<any>} - The result of the method call.
 */
async function queryContractState(contract, methodName, params = []) {
    const result = await contract[methodName](...params);
    console.log(`Query result for ${methodName}:`, result.toString());
    return result;
}

/**
 * Approves a specified amount of tokens for a contract.
 * @param {Contract} tokenContract - The token contract instance.
 * @param {string} spender - The address to approve.
 * @param {BigNumber} amount - The amount to approve.
 * @param {Object} signer - The signer to send the transaction with.
 * @returns {Promise<TransactionResponse>} - The transaction response.
 */
async function approveTokens(tokenContract, spender, amount, signer) {
    const tx = await tokenContract.connect(signer).approve(spender, amount);
    console.log(`Approval transaction sent: ${tx.hash}`);
    await tx.wait();
    console.log(`Approval confirmed: ${tx.hash}`);
    return tx;
}

/**
 * Retrieves the balance of a specific address for a token contract.
 * @param {Contract} tokenContract - The token contract instance.
 * @param {string} address - The address to check the balance of.
 * @returns {Promise<BigNumber>} - The balance of the address.
 */
async function getTokenBalance(tokenContract, address) {
    const balance = await tokenContract.balanceOf(address);
    console.log(`Balance of ${address}: ${balance.toString()}`);
    return balance;
}

module.exports = {
    deployContract,
    sendTransaction,
    queryContractState,
    approveTokens,
    getTokenBalance,
};
