// Import required modules
const fs = require('fs');
const path = require('path');

// Load environment variables from a .env file
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

// Define the network configurations
const NETWORKS = {
    mainnet: {
        name: 'Ethereum Mainnet',
        chainId: 1,
        rpcUrl: process.env.MAINNET_RPC_URL || 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID',
        explorerUrl: 'https://etherscan.io',
        nativeCurrency: {
            name: 'Ether',
            symbol: 'ETH',
            decimals: 18,
        },
        gasLimit: parseInt(process.env.MAINNET_GAS_LIMIT) || 500000,
        gasPrice: parseInt(process.env.MAINNET_GAS_PRICE) || 20000000000, // 20 Gwei
    },
    rinkeby: {
        name: 'Rinkeby Testnet',
        chainId: 4,
        rpcUrl: process.env.RINKEBY_RPC_URL || 'https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID',
        explorerUrl: 'https://rinkeby.etherscan.io',
        nativeCurrency: {
            name: 'Ether',
            symbol: 'ETH',
            decimals: 18,
        },
        gasLimit: parseInt(process.env.RINKEBY_GAS_LIMIT) || 500000,
        gasPrice: parseInt(process.env.RINKEBY_GAS_PRICE) || 20000000000,
    },
    goerli: {
        name: 'Goerli Testnet',
        chainId: 5,
        rpcUrl: process.env.GOERLI_RPC_URL || 'https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID',
        explorerUrl: 'https://goerli.etherscan.io',
        nativeCurrency: {
            name: 'Ether',
            symbol: 'ETH',
            decimals: 18,
        },
        gasLimit: parseInt(process.env.GOERLI_GAS_LIMIT) || 500000,
        gasPrice: parseInt(process.env.GOERLI_GAS_PRICE) || 20000000000,
    },
    // Additional networks can be added here
};

// Function to get the configuration for a specific network
const getNetworkConfig = (network) => {
    if (!NETWORKS[network]) {
        throw new Error(`Network configuration for "${network}" not found.`);
    }
    return NETWORKS[network];
};

// Function to validate the configuration
const validateConfig = (config) => {
    const requiredFields = ['name', 'chainId', 'rpcUrl', 'explorerUrl', 'nativeCurrency', 'gasLimit', 'gasPrice'];
    requiredFields.forEach(field => {
        if (!config[field]) {
            throw new Error(`Missing required configuration field: ${field}`);
        }
    });
};

// Export the configuration and validation function
module.exports = {
    getNetworkConfig,
    validateConfig,
    NETWORKS,
};
