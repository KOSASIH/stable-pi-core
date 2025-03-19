// Load environment variables from .env file
require('dotenv').config();

// Configuration object
const config = {
    authyApiKey: process.env.AUTHY_API_KEY, // Authy API key for MFA
    port: process.env.PORT || 3000,          // Server port, defaults to 3000
    dbConnectionString: process.env.DB_CONNECTION_STRING, // Database connection string
    logLevel: process.env.LOG_LEVEL || 'info', // Logging level, defaults to 'info'
};

// Validate required configurations
const validateConfig = () => {
    if (!config.authyApiKey) {
        throw new Error('Missing Authy API key. Please set AUTHY_API_KEY in your .env file.');
    }
    if (!config.dbConnectionString) {
        throw new Error('Missing database connection string. Please set DB_CONNECTION_STRING in your .env file.');
    }
};

// Call the validation function
validateConfig();

module.exports = config;
