// config/index.js

import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from a .env file
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const config = {
    environment: process.env.NODE_ENV || 'development',
    port: process.env.PORT || 3000,
    database: {
        host: process.env.DB_HOST || 'localhost',
        port: process.env.DB_PORT || 5432,
        user: process.env.DB_USER || 'user',
        password: process.env.DB_PASSWORD || 'password',
        database: process.env.DB_NAME || 'database',
    },
    jwt: {
        secret: process.env.JWT_SECRET || 'your_jwt_secret',
        expiresIn: process.env.JWT_EXPIRES_IN || '1h',
    },
    quantum: {
        enabled: process.env.QUANTUM_ENABLED === 'true',
        algorithm: process.env.QUANTUM_ALGORITHM || 'SHA512',
    },
    logging: {
        level: process.env.LOG_LEVEL || 'info',
        format: process.env.LOG_FORMAT || 'combined',
    },
};

export default config;
