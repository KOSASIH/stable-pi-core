// src/api/controllers/conversionController.js

const Web3 = require('web3');
const PiConverterABI = require('../../contracts/PiConverter.json'); // Import the ABI of the smart contract
const contractAddress = 'YOUR_CONTRACT_ADDRESS'; // Replace with your deployed contract address

const web3 = new Web3(new Web3.providers.HttpProvider('https://YOUR_INFURA_OR_ALCHEMY_URL')); // Replace with your Infura or Alchemy URL
const contract = new web3.eth.Contract(PiConverterABI, contractAddress);

// Replace with the address of the user interacting with the contract
const userAddress = 'USER_WALLET_ADDRESS'; // Replace with the user's wallet address

// Deposit function
exports.deposit = async (req, res) => {
    const { amount } = req.body;

    try {
        const tx = await contract.methods.deposit(amount).send({ from: userAddress });
        res.status(200).json({ success: true, transaction: tx });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, message: 'Deposit failed', error });
    }
};

// Convert function
exports.convert = async (req, res) => {
    const { amount } = req.body;

    try {
        const tx = await contract.methods.convert(amount).send({ from: userAddress });
        res.status(200).json({ success: true, transaction: tx });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, message: 'Conversion failed', error });
    }
};

// Check balance function
exports.checkBalance = async (req, res) => {
    try {
        const balance = await contract.methods.checkBalance().call({ from: userAddress });
        res.status(200).json({ success: true, balance });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, message: 'Failed to retrieve balance', error });
    }
};
