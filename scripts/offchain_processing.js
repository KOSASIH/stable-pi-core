// scripts/offchain_processing.js

const { create } = require('ipfs-http-client');
const { ethers } = require('ethers');
require('dotenv').config(); // Load environment variables from .env file

// Initialize IPFS client
const ipfs = create({ url: 'https://ipfs.infura.io:5001' });

// Connect to Ethereum network
const provider = new ethers.providers.JsonRpcProvider(process.env.INFURA_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
const oracleContractAddress = process.env.ORACLE_CONTRACT_ADDRESS;
const oracleABI = require('./OracleABI.json'); // Import the ABI of the Oracle contract
const oracleContract = new ethers.Contract(oracleContractAddress, oracleABI, wallet);

// Function to store data on IPFS
async function storeDataOnIPFS(data) {
    try {
        const { cid } = await ipfs.add(JSON.stringify(data));
        console.log(`Data stored on IPFS with CID: ${cid}`);
        return cid.toString();
    } catch (error) {
        console.error('Error storing data on IPFS:', error);
        throw error;
    }
}

// Function to submit data to the Oracle contract
async function submitDataToOracle(dataType, data) {
    try {
        const tx = await oracleContract.submitData(dataType, data);
        await tx.wait(); // Wait for the transaction to be mined
        console.log(`Data submitted to Oracle: ${dataType} - ${data}`);
    } catch (error) {
        console.error('Error submitting data to Oracle:', error);
        throw error;
    }
}

// Main function to handle off-chain processing
async function main() {
    // Example data to process
    const dataToProcess = {
        price: 3000,
        timestamp: new Date().toISOString(),
        source: 'Edge Node',
    };

    // Step 1: Store data on IPFS
    const cid = await storeDataOnIPFS(dataToProcess);

    // Step 2: Submit the CID to the Oracle contract
    await submitDataToOracle('ETH/USD', cid);
}

// Execute the main function
main()
    .then(() => console.log('Off-chain processing completed successfully.'))
    .catch((error) => console.error('Error in off-chain processing:', error));
