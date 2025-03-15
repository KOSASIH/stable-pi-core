// stable-pi-core/api-gateway/index.js

const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');
const bodyParser = require('body-parser');
const axios = require('axios');
const rateLimit = require('express-rate-limit');
const cors = require('cors');
const dotenv = require('dotenv');
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json'); // Assuming you have a swagger.json file

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(cors()); // Enable CORS
app.use(bodyParser.json());

// Rate limiting middleware
const limiter = rateLimit({
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests, please try again later.',
});
app.use(limiter);

// Swagger documentation
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// RESTful API Example
app.get('/api/blockchain/:chainId', async (req, res) => {
    const { chainId } = req.params;
    try {
        const response = await axios.get(`https://api.example.com/blockchain/${chainId}`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching blockchain data:', error);
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
