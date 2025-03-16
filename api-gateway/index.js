// stable-pi-core/api-gateway/index.js

const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');
const bodyParser = require('body-parser');
const axios = require('axios');
const rateLimit = require('express-rate-limit');
const cors = require('cors');
const dotenv = require('dotenv');
const swaggerUi = require('swagger-ui-express');
const helmet = require('helmet');
const morgan = require('morgan'); // For logging
const EthereumAdapter = require('./adapters/ethereumAdapter');
const BitcoinAdapter = require('./adapters/bitcoinAdapter'); // Example for another blockchain
// Import other adapters as needed

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

// Initialize Adapters
const ethereumAdapter = new EthereumAdapter(process.env.ETHEREUM_API_URL || 'https://api.etherscan.io/api');
const bitcoinAdapter = new BitcoinAdapter(process.env.BITCOIN_API_URL || 'https://api.blockcypher.com/v1/btc/main');
// Initialize other adapters as needed

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // Enable CORS
app.use(bodyParser.json());
app.use(morgan('combined')); // Logging

// Rate limiting middleware
const limiter = rateLimit({
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests, please try again later.',
});
app.use(limiter);

// Swagger documentation
const swaggerDocument = require('./swagger.json'); // Assuming you have a swagger.json file
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// RESTful API Example: Fetch Ethereum Block Data
app.get('/api/ethereum/block/:blockNumber', async (req, res) => {
    const { blockNumber } = req.params;
    try {
        const blockData = await ethereumAdapter.getBlock(blockNumber);
        res.json(blockData);
    } catch (error) {
        console.error('Error fetching Ethereum block:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// RESTful API Example: Fetch Bitcoin Block Data
app.get('/api/bitcoin/block/:blockHeight', async (req, res) => {
    const { blockHeight } = req.params;
    try {
        const blockData = await bitcoinAdapter.getBlock(blockHeight);
        res.json(blockData);
    } catch (error) {
        console.error('Error fetching Bitcoin block:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// RESTful API Example: Fetch Transaction Data
app.get('/api/ethereum/transaction/:transactionHash', async (req, res) => {
    const { transactionHash } = req.params;
    try {
        const transactionData = await ethereumAdapter.getTransaction(transactionHash);
        res.json(transactionData);
    } catch (error) {
        console.error('Error fetching Ethereum transaction:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// RESTful API Example: Call Smart Contract Method
app.post('/api/ethereum/contract/:contractAddress/call', async (req, res) => {
    const { contractAddress } = req.params;
    const { methodName, params } = req.body;

    if (!methodName || !Array.isArray(params)) {
        return res.status(400).json({ error: 'Method name and parameters are required.' });
    }

    try {
        const result = await ethereumAdapter.callContractMethod(contractAddress, methodName, params);
        res.json(result);
    } catch (error) {
        console.error('Error calling contract method:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// GraphQL Schema Definition
const typeDefs = gql`
    type Query {
        blockchainData(chainId: String!): BlockchainData
    }

    type BlockchainData {
        id: String
        name: String
        transactions: [Transaction]
    }

    type Transaction {
        hash: String
        from: String
        to: String
        value: Float
    }
`;

// GraphQL Resolvers
const resolvers = {
    Query: {
        blockchainData: async (_, { chainId }) => {
            try {
                const response = await axios.get(`https://api.example.com/blockchain/${chainId}`);
                return response.data; // Adjust based on the API response structure
            } catch (error) {
                console.error('Error fetching blockchain data:', error);
                throw new Error('Failed to fetch blockchain data');
            }
        },
    },
};

// Apollo Server Setup
const server = new ApolloServer({ typeDefs, resolvers });
server.applyMiddleware({ app });

// Start the Express server
app.listen(PORT, () => {
    console.log(`API Gateway running at http://localhost:${PORT}`);
    console.log(`GraphQL endpoint at http://localhost:${PORT}${server.graphqlPath}`);
    console.log(`API documentation available at http://localhost:${PORT}/api-docs`);
});
