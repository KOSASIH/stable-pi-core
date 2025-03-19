// truffle-config.js

const HDWalletProvider = require('@truffle/hdwallet-provider');
const Web3 = require('web3');
require('dotenv').config(); // Load environment variables from .env file

const MNEMONIC = process.env.MNEMONIC; // Your wallet mnemonic
const INFURA_PROJECT_ID = process.env.INFURA_PROJECT_ID; // Infura project ID
const INFURA_URL = `https://rinkeby.infura.io/v3/${INFURA_PROJECT_ID}`; // Rinkeby testnet URL
const MAINNET_URL = `https://mainnet.infura.io/v3/${INFURA_PROJECT_ID}`; // Mainnet URL

module.exports = {
  // Configure networks
  networks: {
    development: {
      host: "127.0.0.1", // Localhost (default: none)
      port: 7545, // Ganache port (default: none)
      network_id: "*", // Any network (default: none)
    },
    rinkeby: {
      provider: () => new HDWalletProvider(MNEMONIC, INFURA_URL),
      network_id: 4, // Rinkeby's id
      gas: 5500000, // Gas limit
      confirmations: 2, // # of confirmations to wait between deployments
      timeoutBlocks: 200, // # of blocks before a deployment times out
      skipDryRun: true // Skip dry run before migrations? (default: false for public nets)
    },
    mainnet: {
      provider: () => new HDWalletProvider(MNEMONIC, MAINNET_URL),
      network_id: 1, // Mainnet's id
      gas: 5500000, // Gas limit
      confirmations: 2, // # of confirmations to wait between deployments
      timeoutBlocks: 200, // # of blocks before a deployment times out
      skipDryRun: true // Skip dry run before migrations? (default: false for public nets)
    }
  },

  // Configure compilers
  compilers: {
    solc: {
      version: "0.8.19", // Specify the Solidity version
      settings: {
        optimizer: {
          enabled: true, // Enable optimization
          runs: 200 // Optimize for how many times you intend to run the code
        },
        evmVersion: "istanbul" // Specify the EVM version
      }
    }
  },

  // Configure plugins
  plugins: [
    'truffle-plugin-verify', // Plugin for verifying contracts on Etherscan
    'truffle-contract-size' // Plugin for checking contract sizes
  ],

  // Configure Mocha testing framework
  mocha: {
    timeout: 100000 // Set timeout for tests
  },

  // Configure the build directory
  contracts_build_directory: './build/contracts',

  // Configure the migrations directory
  migrations_directory: './migrations',

  // Configure the test directory
  test_directory: './test',

  // Configure the artifacts directory
  artifacts_directory: './artifacts'
};
