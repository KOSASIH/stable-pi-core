// config/web3.js

const Web3 = require('web3');
require('dotenv').config();

let web3;

if (process.env.NODE_ENV === 'development') {
    // Connect to local Ethereum node
    web3 = new Web3('http://localhost:8545'); // Adjust the port if necessary
} else {
    // Connect to a remote Ethereum node (e.g., Infura)
    const provider = new Web3.providers.HttpProvider(process.env.INFURA_URL);
    web3 = new Web3(provider);
}

module.exports = web3;
