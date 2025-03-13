// utils/constants.js

// Environment Configuration
const ENV = process.env.NODE_ENV || 'development';

// Ethereum Network IDs
export const NETWORK_IDS = {
    MAINNET: 1,
    ROPSTEN: 3,
    RINKEBY: 4,
    GOERLI: 5,
    KOVAN: 42,
    POLYGON_MAINNET: 137,
    POLYGON_MUMBAI: 80001,
    BSC_MAINNET: 56,
    BSC_TESTNET: 97,
};

// Contract Addresses
export const ADDRESSES = {
    STABLE_PI_CORE: {
        [NETWORK_IDS.MAINNET]: "0xYourStablePiCoreAddressHere",
        [NETWORK_IDS.ROPSTEN]: "0xYourStablePiCoreAddressHere",
        [NETWORK_IDS.POLYGON_MAINNET]: "0xYourStablePiCoreAddressHere",
        [NETWORK_IDS.BSC_MAINNET]: "0xYourStablePiCoreAddressHere",
    },
    ORACLE_CONTRACT: {
        [NETWORK_IDS.MAINNET]: "0xYourOracleContractAddressHere",
        [NETWORK_IDS.ROPSTEN]: "0xYourOracleContractAddressHere",
        [NETWORK_IDS.POLYGON_MAINNET]: "0xYourOracleContractAddressHere",
        [NETWORK_IDS.BSC_MAINNET]: "0xYourOracleContractAddressHere",
    },
    PROXY_CONTRACT: {
        [NETWORK_IDS.MAINNET]: "0xYourProxyContractAddressHere",
        [NETWORK_IDS.ROPSTEN]: "0xYourProxyContractAddressHere",
        [NETWORK_IDS.POLYGON_MAINNET]: "0xYourProxyContractAddressHere",
        [NETWORK_IDS.BSC_MAINNET]: "0xYourProxyContractAddressHere",
    },
};

// Token Metadata
export const TOKEN_METADATA = {
    STABLE_TOKEN: {
        symbol: "STBL",
        name: "Stable Token",
        decimals: 18,
        address: ADDRESSES.STABLE_PI_CORE[NETWORK_IDS.MAINNET], // Example for mainnet
    },
    ORACLE_TOKEN: {
        symbol: "ORCL",
        name: "Oracle Token",
        decimals: 18,
        address: ADDRESSES.ORACLE_CONTRACT[NETWORK_IDS.MAINNET], // Example for mainnet
    },
};

// Commonly Used Values
export const DECIMALS = 18;
export const MAX_UINT256 = "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"; // 2^256 - 1

// Error Codes
export const ERROR_CODES = {
    INVALID_ADDRESS: "ERR_INVALID_ADDRESS",
    INSUFFICIENT_FUNDS: "ERR_INSUFFICIENT_FUNDS",
    UNAUTHORIZED: "ERR_UNAUTHORIZED",
    NETWORK_ERROR: "ERR_NETWORK_ERROR",
};

// API Endpoints
export const API_ENDPOINTS = {
    ORACLE: {
        [NETWORK_IDS.MAINNET]: "https://api.mainnet.oracle.com",
        [NETWORK_IDS.ROPSTEN]: "https://api.ropsten.oracle.com",
        [NETWORK_IDS.POLYGON_MAINNET]: "https://api.polygon.oracle.com",
        [NETWORK_IDS.BSC_MAINNET]: "https://api.bsc.oracle.com",
    },
};

// Feature Flags
export const FEATURE_FLAGS = {
    ENABLE_NEW_FEATURE: ENV === 'development', // Enable new features only in development
    USE_MOCK_ORACLE: ENV === 'test', // Use mock oracle in testing
};

// Gas Configuration
export const GAS_LIMIT = 3000000; // Default gas limit for transactions
export const DEFAULT_TIMEOUT = 30000; // Default timeout for async operations in milliseconds

// Logging Configuration
export const LOGGING_LEVEL = ENV === 'production' ? 'error' : 'debug'; // Set logging level based on environment
