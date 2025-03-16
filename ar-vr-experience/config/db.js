// ar-vr-experience/config/db.js

const mongoose = require('mongoose');
const { Pool } = require('pg'); // PostgreSQL client
const dotenv = require('dotenv');
const winston = require('winston'); // For logging

dotenv.config();

// Logger configuration
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'db.log' })
    ],
});

// Database configuration
const dbConfig = {
    type: process.env.DB_TYPE || 'mongodb', // 'mongodb' or 'postgres'
    mongodbURI: process.env.MONGODB_URI || 'mongodb://localhost:27017/arvr-experience',
    postgresConfig: {
        user: process.env.PG_USER || 'user',
        host: process.env.PG_HOST || 'localhost',
        database: process.env.PG_DATABASE || 'arvr_experience',
        password: process.env.PG_PASSWORD || 'password',
        port: process.env.PG_PORT || 5432,
    },
};

// MongoDB connection
const connectMongoDB = async () => {
    try {
        await mongoose.connect(dbConfig.mongodbURI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        logger.info('MongoDB connected successfully');
    } catch (error) {
        logger.error('Error connecting to MongoDB:', error);
        process.exit(1); // Exit the process with failure
    }
};

// PostgreSQL connection
const pool = new Pool(dbConfig.postgresConfig);

const connectPostgreSQL = async () => {
    try {
        await pool.connect();
        logger.info('PostgreSQL connected successfully');
    } catch (error) {
        logger.error('Error connecting to PostgreSQL:', error);
        process.exit(1); // Exit the process with failure
    }
};

// Function to connect to the database
const connectDB = async () => {
    if (dbConfig.type === 'mongodb') {
        await connectMongoDB();
    } else if (dbConfig.type === 'postgres') {
        await connectPostgreSQL();
    } else {
        throw new Error(`Database type ${dbConfig.type} is not supported.`);
    }
};

// Function to disconnect from the database
const disconnectDB = async () => {
    if (dbConfig.type === 'mongodb') {
        await mongoose.disconnect();
        logger.info('MongoDB disconnected successfully');
    } else if (dbConfig.type === 'postgres') {
        await pool.end();
        logger.info('PostgreSQL disconnected successfully');
    }
};

// Function to execute a query in PostgreSQL
const executeQuery = async (query, params) => {
    try {
        const res = await pool.query(query, params);
        return res.rows;
    } catch (error) {
        logger.error('Error executing query:', error);
        throw new Error('Database query failed');
    }
};

// Export the connection functions and query execution
module.exports = {
    connectDB,
    disconnectDB,
    executeQuery,
};
