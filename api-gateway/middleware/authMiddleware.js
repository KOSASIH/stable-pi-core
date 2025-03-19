// stable-pi-core/api-gateway/middleware/authMiddleware.js

const jwt = require('jsonwebtoken');

// Middleware function to authenticate requests using JWT
const authMiddleware = (req, res, next) => {
    // Get the token from the Authorization header
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer <token>

    if (!token) {
        return res.status(401).json({ error: 'Access token is required.' });
    }

    // Verify the token
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Invalid access token.' });
        }

        // Attach the user information to the request object
        req.user = user;
        next(); // Proceed to the next middleware or route handler
    });
};

module.exports = authMiddleware;
