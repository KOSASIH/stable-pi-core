// stable-pi-core/api-gateway/adapters/cosmosAdapter.js

const { StargateClient, SigningStargateClient, assertIsBroadcastTxSuccess } = require('@cosmjs/stargate');
const { DirectSecp256k1Wallet, Registry, AminoTypes } = require('@cosmjs/proto-signing');
require('dotenv').config();

const COSMOS_API_URL = process.env.COSMOS_API_URL || 'https://rpc.cosmos.network'; // Set your Cosmos API URL in .env

// Initialize the Cosmos client
let client;
let signingClient;

async function init() {
    client = await StargateClient.connect(COSMOS_API_URL);
}

/**
 * Get the balance of a given Cosmos address.
 * @param {string} address - The Cosmos address to check.
 * @returns {Promise<number>} - The balance in tokens.
 */
async function getBalance(address) {
    try {
        const balance = await client.getAllBalances(address);
        return balance; // Return balance in tokens
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send tokens from one address to another.
 * @param {string} fromAddress - The sender's Cosmos address.
 * @param {string} toAddress - The recipient's Cosmos address.
 * @param {number} amount - The amount of tokens to send.
 * @param {string} denom - The token denomination (e.g., 'uatom' for ATOM).
 * @param {string} senderMnemonic - The sender's mnemonic.
 * @returns {Promise<string>} - The transaction hash.
 */
async function sendTokens(fromAddress, toAddress, amount, denom, senderMnemonic) {
    const wallet = await DirectSecp256k1Wallet.fromMnemonic(senderMnemonic);
    const accounts = await wallet.getAccounts();
    const account = accounts[0];

    signingClient = await SigningStargateClient.connectWithSigner(COSMOS_API_URL, wallet);

    try {
        const fee = {
            amount: [{
                denom: denom,
                amount: '5000', // Fee amount in the same denomination
            }],
            gas: '200000', // Gas limit
        };

        const result = await signingClient.sendTokens(fromAddress, toAddress, [{
            denom: denom,
            amount: amount.toString(),
        }], fee, 'Sending tokens');

        assertIsBroadcastTxSuccess(result); // Ensure the transaction was successful
        return result.transactionHash; // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to send tokens: ${error.message}`);
    }
}

/**
 * Monitor transaction status until confirmed.
 * @param {string} txHash - The transaction hash to monitor.
 * @returns {Promise<Object>} - The transaction status.
 */
async function monitorTransaction(txHash) {
    let confirmed = false;
    let attempts = 0;

    while (!confirmed && attempts < 10) {
        attempts++;
        const transaction = await client.getTx(txHash);
        if (transaction && transaction.code === 0) {
            confirmed = true;
            return { txHash, status: 'confirmed' };
        }
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for 5 seconds before checking again
    }

    throw new Error(`Transaction ${txHash} not confirmed after multiple attempts.`);
}

/**
 * Fetch transaction details by transaction hash.
 * @param {string} txHash - The transaction hash to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txHash) {
    try {
        const transaction = await client.getTx(txHash);
        return transaction; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

/**
 * Interact with a smart contract (CosmWasm).
 * @param {string} contractAddress - The address of the smart contract.
 * @param {Object} params - The parameters to pass to the contract.
 * @param {string} senderMnemonic - The sender's mnemonic.
 * @returns {Promise<string>} - The transaction hash.
 */
async function interactWithContract(contractAddress, params, senderMnemonic) {
    const wallet = await DirectSecp256k1Wallet.fromMnemonic(senderMnemonic);
    const accounts = await wallet.getAccounts();
    const account = accounts[0];

    signingClient = await SigningStargateClient.connectWithSigner(COSMOS_API_URL, wallet);

    try {
        const result = await signingClient.execute(account.address, contractAddress, params, 'auto', undefined, undefined);
        assertIsBroadcastTxSuccess(result); // Ensure the transaction was successful
        return result.transactionHash; // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to interact with contract: ${error.message}`);
    }
}

// Initialize the adapter
init().catch(console.error);

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendTokens,
    monitorTransaction,
    getTransactionDetails,
    interactWithContract,
};
