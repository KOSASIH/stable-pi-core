// src/space/trqf.js
const express = require('express');
const bodyParser = require('body-parser');
const Web3 = require('web3');
const { body, validationResult } = require('express-validator');
const morgan = require('morgan');
const { createSimulation, getSimulationResults } = require('./simulationEngine'); // Assume these functions are defined in simulationEngine.js

const app = express();
app.use(bodyParser.json());
app.use(morgan('combined')); // Logging middleware

// Load environment variables
const ETH_NODE_URL = process.env.ETH_NODE_URL || 'https://your.ethereum.node';
const WALLET_ADDRESS = process.env.WALLET_ADDRESS || 'your_wallet_address';
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS || 'contract_address';

const web3 = new Web3(ETH_NODE_URL); // Connect to Ethereum node

// API Endpoint to start a simulation
app.post('/api/simulate', [
  body('strategy').isString().notEmpty().withMessage('Strategy is required')
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { strategy } = req.body;
  try {
    const simulationId = await createSimulation(strategy);
    res.status(201).send({ message: 'Simulation started', simulationId });
  } catch (error) {
    console.error('Error starting simulation:', error);
    res.status(500).send('Failed to start simulation');
  }
});

// API Endpoint to get simulation results
app.get('/api/simulation/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const results = await getSimulationResults(id);
    res.send({ results });
  } catch (error) {
    console.error('Error fetching simulation results:', error);
    res.status(500).send('Failed to fetch results');
  }
});

// API Endpoint to record results on the blockchain
app.post('/api/record', [
  body('simulationId').isString().notEmpty().withMessage('Simulation ID is required'),
  body('results').isArray().notEmpty().withMessage('Results are required')
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { simulationId, results } = req.body;
  try {
    const transaction = await web3.eth.sendTransaction({
      from: WALLET_ADDRESS,
      to: CONTRACT_ADDRESS,
      data: web3.utils.toHex(JSON.stringify({ simulationId, results })),
    });

    // Wait for transaction confirmation
    const receipt = await web3.eth.getTransactionReceipt(transaction.transactionHash);
    if (receipt && receipt.status) {
      res.send({ message: 'Results recorded on blockchain', transaction });
    } else {
      res.status(500).send('Transaction failed');
    }
  } catch (error) {
    console.error('Error recording results:', error);
    res.status(500).send('Failed to record results');
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`TRQF server running on port ${PORT}`);
});
