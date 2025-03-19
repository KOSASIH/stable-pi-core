// stable-pi-core/api-gateway/graphql/schema.js

const { gql } = require('apollo-server-express');

// Define the GraphQL schema
const typeDefs = gql`
    # Define the Transaction type
    type Transaction {
        hash: String!
        from: String!
        to: String!
        value: Float!
        blockNumber: String!
        gas: String
        gasPrice: String
        input: String
    }

    # Define the Block type
    type Block {
        number: String!
        hash: String!
        parentHash: String!
        transactions: [Transaction]!
        timestamp: String
    }

    # Define the Query type
    type Query {
        # Ethereum Queries
        ethereumBlock(blockNumber: String!): Block
        ethereumTransaction(transactionHash: String!): Transaction

        # Bitcoin Queries
        bitcoinBlock(blockHeight: String!): Block
        bitcoinTransaction(transactionHash: String!): Transaction
        bitcoinPrice: Float
    }
`;

module.exports = typeDefs;
