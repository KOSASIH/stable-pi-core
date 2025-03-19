// stable-pi-core/api-gateway/middleware/loggingMiddleware.js

const morgan = require('morgan');

// Create a logging middleware using morgan
const loggingMiddleware = morgan('combined', {
    // Customize the logging format
    skip: (req, res) => {
        return res.statusCode < 400; // Skip logging for successful responses (status < 400)
    },
    stream: {
        write: (message) => {
            // Here you can write the log to a file or a logging service
            console.log(message.trim()); // For demonstration, we log to the console
        }
    }
});

module.exports = loggingMiddleware;
