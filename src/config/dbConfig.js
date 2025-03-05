const mongoose = require('mongoose');

// Database configuration
const dbConfig = {
    uri: process.env.DB_URI || 'mongodb://localhost:27017/piCoinDB', // Default to local MongoDB
    options: {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        useCreateIndex: true,
        useFindAndModify: false,
    },
};

// Function to connect to the database
const connectDB = async () => {
    try {
        await mongoose.connect(dbConfig.uri, dbConfig.options);
        console.log('MongoDB connected successfully');
    } catch (error) {
        console.error(`MongoDB connection error: ${error.message}`);
        process.exit(1); // Exit process with failure
    }
};

module.exports = {
    dbConfig,
    connectDB,
};
