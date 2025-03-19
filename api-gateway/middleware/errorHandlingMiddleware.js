// stable-pi-core/api-gateway/middleware/errorHandlingMiddleware.js

const errorHandlingMiddleware = (err, req, res, next) => {
    // Log the error details (you can customize this to log to a file or external service)
    console.error('Error occurred:', {
        message: err.message,
        stack: err.stack,
        method: req.method,
        url: req.originalUrl,
        body: req.body,
    });

    // Set the response status code based on the error type
    const statusCode = err.statusCode || 500; // Default to 500 if no status code is set

    // Send a standardized error response
    res.status(statusCode).json({
        error: {
            message: err.message || 'Internal Server Error',
            status: statusCode,
        },
    });
};

module.exports = errorHandlingMiddleware;
