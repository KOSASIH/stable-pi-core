// Import required modules
const express = require('express');
const bodyParser = require('body-parser');
const morgan = require('morgan'); // For logging requests
const authRoutes = require('./routes/authRoutes');
const config = require('./config/config');

// Initialize the Express application
const app = express();

// Middleware setup
app.use(bodyParser.json()); // Parse JSON request bodies
app.use(morgan('dev')); // Log requests to the console

// Use the authentication routes
app.use('/auth', authRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ success: false, message: 'Internal Server Error', error: err.message });
});

// Start the server
const PORT = config.port;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
