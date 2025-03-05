// API configuration
const apiConfig = {
    port: process.env.PORT || 3000, // Default to port 3000
    baseUrl: process.env.BASE_URL || 'http://localhost:3000', // Default base URL
    apiVersion: 'v1', // API version
};

// Export the configuration
module.exports = apiConfig;
