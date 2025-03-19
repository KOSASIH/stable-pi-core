// stable-pi-core/api-gateway/adapters/solanaAdapter.js

const {
    Connection,
    PublicKey,
    clusterApiUrl,
    Keypair,
    LAMPORTS_PER_SOL,
    Transaction,
    SystemProgram,
    sendAndConfirmTransaction,
} = require('@solana/web3.js');
require('dotenv').config();

const SOLANA_API_URL = process.env.SOLANA_API_URL || clusterApiUrl('devnet'); // Set your Solana API URL in .env or use devnet

// Initialize the Solana connection
const connection = new Connection(SOLANA_API_URL, 'confirmed');

/**
 * Get the balance of a given Solana address.
 * @param {string} address - The Solana address to check.
 * @returns {Promise<number>} - The balance in SOL.
 */
async function getBalance(address) {
    try {
        const publicKey = new PublicKey(address);
        const balance = await connection.getBalance(publicKey);
        return balance / LAMPORTS_PER_SOL; // Convert lamports to SOL
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send SOL from one address to another.
 * @param {string} fromAddress - The sender's Solana address.
 * @param {string} toAddress - The recipient's Solana address.
 * @param {number} amount - The amount of SOL to send.
 * @param {string} senderPrivateKey - The sender's private key (base58 encoded).
 * @returns {Promise<string>} - The transaction signature.
 */
async function sendSOL(fromAddress, toAddress, amount, senderPrivateKey) {
    const fromKeypair = Keypair.fromSecretKey(Uint8Array.from(JSON.parse(senderPrivateKey)));

    try {
        const transaction = new Transaction().add(
            SystemProgram.transfer({
                fromPubkey: fromKeypair.publicKey,
                toPubkey: new PublicKey(toAddress),
                lamports: amount * LAMPORTS_PER_SOL, // Convert SOL to lamports
            })
        );

        const signature = await sendAndConfirmTransaction(connection, transaction, [fromKeypair]);
        return signature; // Return the transaction signature
    } catch (error) {
        throw new Error(`Failed to send SOL: ${error.message}`);
    }
}

/**
 * Monitor transaction status until confirmed.
 * @param {string} txSignature - The transaction signature to monitor.
 * @returns {Promise<Object>} - The transaction status.
 */
async function monitorTransaction(txSignature) {
    let confirmed = false;
    let attempts = 0;

    while (!confirmed && attempts < 10) {
        attempts++;
        const transactionStatus = await connection.getSignatureStatus(txSignature);
        if (transactionStatus && transactionStatus.confirmationStatus === 'confirmed') {
            confirmed = true;
            return { txSignature, status: 'confirmed' };
        }
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for 5 seconds before checking again
    }

    throw new Error(`Transaction ${txSignature} not confirmed after multiple attempts.`);
}

/**
 * Fetch transaction details by transaction signature.
 * @param {string} txSignature - The transaction signature to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txSignature) {
    try {
        const transactionDetails = await connection.getTransaction(txSignature);
        return transactionDetails; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

/**
 * Interact with a Solana program (smart contract).
 * @param {string} programId - The ID of the Solana program.
 * @param {Array} params - The parameters to pass to the program.
 * @returns {Promise<string>} - The transaction signature.
 */
async function interactWithProgram(programId, params) {
    // Implement interaction logic with the Solana program
    // This is a placeholder; you will need to use a library or method to interact with the program
    // Return the transaction signature
    return 'transaction_signature_placeholder'; // Placeholder
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendSOL,
    monitorTransaction,
    getTransactionDetails,
    interactWithProgram,
};
