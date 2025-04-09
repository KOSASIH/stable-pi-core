// src/tests/trqf.test.js
const request = require('supertest');
const express = require('express');
const bodyParser = require('body-parser');
const Web3 = require('web3');
const { body, validationResult } = require('express-validator');
const morgan = require('morgan');
const { createSimulation, getSimulationResults } = require('./simulationEngine'); // Assume these functions are defined in simulationEngine.js

const app = express();
app.use(bodyParser.json());
app.use(morgan('combined')); // Logging middleware

// Mock the Web3 library
jest.mock('web3', () => {
  return jest.fn().mockImplementation(() => {
    return {
      eth: {
        sendTransaction: jest.fn().mockResolvedValue({ transactionHash: 'mockTransactionHash' }),
        getTransactionReceipt: jest.fn().mockResolvedValue({ status: true }),
      },
    };
  });
});

// Mock the simulation engine functions
jest.mock('./simulationEngine', () => ({
  createSimulation: jest.fn().mockResolvedValue('mockSimulationId'),
  getSimulationResults: jest.fn().mockResolvedValue([{ result: 'mockResult' }]),
}));

// Load environment variables
process.env.ETH_NODE_URL = 'https://your.ethereum.node';
process.env.WALLET_ADDRESS = 'your_wallet_address';
process.env.CONTRACT_ADDRESS = 'contract_address';

// Initialize Web3
const Web3 = require('web3');
const web3 = new Web3(process.env.ETH_NODE_URL);

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
      from: process.env.WALLET_ADDRESS,
      to: process.env.CONTRACT_ADDRESS,
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

// Test Suite
describe('Trans-Reality Quantum Forge API', () => {
  test('should start a simulation successfully', async () => {
    const response = await request(app)
      .post('/api/simulate')
      .send({ strategy: 'Test Strategy' });

    expect(response.status).toBe(201);
    expect(response.body.message).toBe('Simulation started');
    expect(response.body.simulationId).toBe('mockSimulationId');
  });

  test('should return validation error for missing strategy', async () => {
    const response = await request(app)
      .post('/api/simulate')
      .send({});

    expect(response.status).toBe(400);
    expect(response.body.errors).toEqual(expect.arrayContaining([
      expect.objectContaining({ msg: 'Strategy is required' })
    ]));
  });

  test('should fetch simulation results successfully', async () => {
    const response = await request(app)
      .get('/api/simulation/mockSimulationId');

    expect(response.status).toBe(200);
    expect(response.body.results).toEqual([{ result: 'mockResult' }]);
  });

  test('should record results on the blockchain successfully', async () => {
    const response = await request(app)
      .post('/api/record')
      .send({ simulationId: 'mockSimulationId', results: ['result1', 'result2'] });

    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Results recorded on blockchain');
    expect(response.body.transaction.transactionHash).toBe('mockTransactionHash');
  });

  test('should return error for missing simulation ID in record', async () => {
    const response = await request(app)
      .post('/api/record')
      .send({ results: ['result1', 'result2'] });

    expect(response.status).toBe(400);
    expect(response.body.errors).toEqual(expect.arrayContaining([
      expect.objectContaining({ msg: 'Simulation ID is required' })
    ]));
  });

  test('should return error for missing results in record', async () => {
    const response = await request(app)
      .post('/api/record')
      .send({ simulationId: 'mockSimulationId' });

    expect(response.status).toBe(400);
    expect(response.body.errors).toEqual(expect.arrayContaining([
      expect.objectContaining({ msg: 'Results are required' })
    ]));
  });
});
