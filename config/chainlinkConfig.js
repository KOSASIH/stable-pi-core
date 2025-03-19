// Import required modules
const fs = require('fs');
const path = require('path');

// Load environment variables from a .env file
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

// Define the network configurations
const NETWORKS = {
    mainnet: {
        chainlinkNodeUrl: process.env.MAINNET_CHAINLINK_NODE_URL || 'https://mainnet.chain.link',
        oracleAddress: process.env.MAINNET_ORACLE_ADDRESS || '0xYourMainnetOracleAddress',
        linkTokenAddress: process.env.MAINNET_LINK_TOKEN_ADDRESS || '0xYourMainnetLinkTokenAddress',
        ccipAddress: process.env.MAINNET_CCIP_ADDRESS || '0xYourMainnetCcipAddress',
        gasLimit: parseInt(process.env.MAINNET_GAS_LIMIT) || 500000,
        gasPrice: parseInt(process.env.MAINNET_GAS_PRICE) || 20000000000, // 20 Gwei
    },
    rinkeby: {
        chainlinkNodeUrl: process.env.RINKEBY_CHAINLINK_NODE_URL || 'https://rinkeby.chain.link',
        oracleAddress: process.env.RINKEBY_ORACLE_ADDRESS || '0xYourRinkebyOracleAddress',
        linkTokenAddress: process.env.RINKEBY_LINK_TOKEN_ADDRESS || '0xYourRinkebyLinkTokenAddress',
        ccipAddress: process.env.RINKEBY_CCIP_ADDRESS || '0xYourRinkebyCcipAddress',
        gasLimit: parseInt(process.env.RINKEBY_GAS_LIMIT) || 500000,
        gasPrice: parseInt(process.env.RINKEBY_GAS_PRICE) || 20000000000,
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
    const requiredFields = ['chainlinkNodeUrl', 'oracleAddress', 'linkTokenAddress', 'ccipAddress', 'gasLimit', 'gasPrice'];
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
};
