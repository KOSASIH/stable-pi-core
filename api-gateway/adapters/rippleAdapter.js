// stable-pi-core/api-gateway/adapters/rippleAdapter.js

const ripple = require('ripple-lib');
require('dotenv').config();

const XRP_API_URL = process.env.XRP_API_URL || 'wss://s1.ripple.com'; // Set your Ripple API URL in .env

// Initialize the Ripple API client
const api = new ripple.RippleAPI({ server: XRP_API_URL });

/**
 * Get the balance of a given Ripple address.
 * @param {string} address - The Ripple address to check.
 * @returns {Promise<number>} - The balance in XRP.
 */
async function getBalance(address) {
    try {
        const accountInfo = await api.getAccountInfo(address);
        return parseFloat(accountInfo.xrpBalance); // Return balance in XRP
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send XRP from one address to another.
 * @param {string} fromAddress - The sender's Ripple address.
 * @param {string} toAddress - The recipient's Ripple address.
 * @param {number} amount - The amount of XRP to send.
 * @param {string} senderSecret - The sender's secret key.
 * @returns {Promise<string>} - The transaction hash.
 */
async function sendXRP(fromAddress, toAddress, amount, senderSecret) {
    try {
        // Prepare the transaction
        const preparedTx = await api.preparePayment(fromAddress, {
            source: {
                address: fromAddress,
                maxAmount: {
                    value: amount.toString(),
                    currency: 'XRP'
                }
            },
            destination: {
                address: toAddress,
                amount: {
                    value: amount.toString(),
                    currency: 'XRP'
                }
            }
        });

        // Sign the transaction
        const signedTx = api.sign(preparedTx.txJSON, senderSecret);

        // Submit the transaction
        const result = await api.submit(signedTx.signedTransaction);
        return result.tx_json.hash; // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to send XRP: ${error.message}`);
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
        const transaction = await api.getTransaction(txHash);
        if (transaction && transaction.outcome.result === 'tesSUCCESS') {
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
        const transaction = await api.getTransaction(txHash);
        return transaction; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

/**
 * Interact with a smart contract (if applicable).
 * @param {string} contractAddress - The address of the smart contract.
 * @param {Object} params - The parameters to pass to the contract.
 * @returns {Promise<string>} - The transaction hash.
 */
async function interactWithContract(contractAddress, params) {
    // Ripple does not have traditional smart contracts like Ethereum,
    // but you can implement logic to interact with payment channels or other features.
    throw new Error('Smart contract interaction is not applicable for Ripple.');
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendXRP,
    monitorTransaction,
    getTransactionDetails,
    interactWithContract,
};
