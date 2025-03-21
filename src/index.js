// src/index.js

import express from 'express';
import bodyParser from 'body-parser';
import morgan from 'morgan'; // For logging requests
import helmet from 'helmet'; // For securing HTTP headers
import rateLimit from 'express-rate-limit'; // For rate limiting
import cors from 'cors'; // For enabling CORS
import authRoutes from './routes/authRoutes';
import config from './config/index';
import { connectToDatabase } from './database'; // Assuming you have a database connection module

// Initialize the Express application
const app = express();

// Middleware setup
app.use(helmet()); // Secure HTTP headers
app.use(cors()); // Enable CORS
app.use(bodyParser.json()); // Parse JSON request bodies
app.use(morgan('dev')); // Log requests to the console

// Rate limiting middleware
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: { success: false, message: 'Too many requests, please try again later.' },
});
app.use(limiter); // Apply rate limiting to all requests

// Use the authentication routes
app.use('/auth', authRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(err.status || 500).json({ success: false, message: err.message || 'Internal Server Error' });
});

// Connect to the database
connectToDatabase()
    .then(() => {
        // Start the server
        const PORT = config.port;
        app.listen(PORT, () => {
            console.log(`Server is running on port ${PORT}`);
        });
    })
    .catch((error) => {
        console.error('Database connection failed:', error);
        process.exit(1); // Exit the process with failure
    });
