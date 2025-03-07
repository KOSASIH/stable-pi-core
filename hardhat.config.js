require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-ethers");
require("dotenv").config(); // For loading environment variables

// This is a sample Hardhat configuration file
module.exports = {
    solidity: {
        version: "0.8.0", // Specify the Solidity version
        settings: {
            optimizer: {
                enabled: true, // Enable the optimizer
                runs: 200, // Optimize for how many times you intend to run the code
            },
        },
    },
    networks: {
        hardhat: {
            chainId: 1337, // Default Hardhat network chain ID
        },
        rinkeby: {
            url: process.env.RINKEBY_URL, // Infura or Alchemy URL for Rinkeby
            accounts: [process.env.PRIVATE_KEY], // Private key for deploying contracts
        },
        mainnet: {
            url: process.env.MAINNET_URL, // Infura or Alchemy URL for Mainnet
            accounts: [process.env.PRIVATE_KEY], // Private key for deploying contracts
        },
        // Add more networks as needed
    },
    etherscan: {
        apiKey: process.env.ETHERSCAN_API_KEY, // Etherscan API key for contract verification
    },
    mocha: {
        timeout: 20000, // Set timeout for tests
    },
};
