// src/tests/acsa.test.js
const request = require('supertest');
const express = require('express');
const bodyParser = require('body-parser');
const tf = require('@tensorflow/tfjs');
const { body, validationResult } = require('express-validator');
const morgan = require('morgan');

const app = express();
app.use(bodyParser.json());
app.use(morgan('combined')); // Logging middleware

let cosmicEntities = [];
let model;

// Mock the TensorFlow model
jest.mock('@tensorflow/tfjs', () => ({
  loadLayersModel: jest.fn(),
  tensor: jest.fn(),
  fit: jest.fn(),
  predict: jest.fn().mockReturnValue({
    arraySync: jest.fn().mockReturnValue([1, 2, 3]) // Mock prediction output
  })
}));

// Load or create a machine learning model
async function loadModel(modelPath) {
  try {
    model = await tf.loadLayersModel(modelPath);
    console.log('Model loaded successfully');
  } catch (error) {
    console.error('Error loading model:', error);
  }
}

// API Endpoint to register a cosmic entity
app.post('/api/entities', [
  body('name').isString().notEmpty(),
  body('type').isString().notEmpty(),
  body('metadata').optional().isObject()
], (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { name, type, metadata } = req.body;
  cosmicEntities.push({ name, type, metadata: metadata || {} });
  res.status(201).send({ message: 'Entity registered', entity: { name, type, metadata } });
});

// API Endpoint to interact with a cosmic entity
app.post('/api/interact', [
  body('entityName').isString().notEmpty(),
  body('data').isArray()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { entityName, data } = req.body;
  const entity = cosmicEntities.find(e => e.name === entityName);
  if (!entity) {
    return res.status(404).send('Entity not found');
  }

  try {
    const processedData = await analyzeData(data);
    res.send({ message: 'Interaction successful', processedData });
  } catch (error) {
    console.error('Error during interaction:', error);
    res.status(500).send('Internal Server Error');
  }
});

// Function to analyze data using the ML model
async function analyzeData(data) {
  try {
    const inputTensor = tf.tensor(data);
    const prediction = model.predict(inputTensor);
    return prediction.arraySync(); // Convert tensor to array
  } catch (error) {
    console.error('Error analyzing data:', error);
    throw new Error('Data analysis failed');
  }
}

// API Endpoint to train the model with new data
app.post('/api/train', [
  body('trainingData').isArray().notEmpty(),
  body('labels').isArray().notEmpty()
], async (req, res) => {
  const { trainingData, labels } = req.body;

  // Placeholder for training logic
  try {
    // Convert training data and labels to tensors
    const inputTensor = tf.tensor(trainingData);
    const labelTensor = tf.tensor(labels);

    // Train the model (this is a simplified example)
    await model.fit(inputTensor, labelTensor, { epochs: 10 });
    res.send({ message: 'Model trained successfully' });
  } catch (error) {
    console.error('Error during model training:', error);
    res.status(500).send('Model training failed');
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`ACSA server running on port ${PORT}`);
  loadModel('path/to/model.json'); // Load the ML model on server start
});

// Test Suite
describe('Astro-Cosmic Sentience Amplifier API', () => {
  beforeAll(async () => {
    await loadModel('path/to/model.json'); // Mock model loading
  });

  afterEach(() => {
    cosmicEntities = []; // Reset entities after each test
  });

  test('should register a cosmic entity', async () => {
    const response = await request(app)
      .post('/api/entities')
      .send({ name: 'Galactic Entity', type: 'Star', metadata: { size: 'large' } });

    expect(response.status).toBe(201);
    expect(response.body.message).toBe('Entity registered');
    expect(response.body.entity.name).toBe('Galactic Entity');
  });

  test('should return validation error for missing entity name', async () => {
    const response = await request(app)
      .post('/api/entities')
      .send({ type: 'Star' });

    expect(response.status).toBe(400);
    expect(response.body.errors).toEqual(expect.arrayContaining([
      expect.objectContaining({ msg: 'Name and type are required' })
    ]));
  });

  test('should interact with a cosmic entity', async () => {
    await request(app)
      .post('/api/entities')
      .send({ name: 'Galactic Entity', type: 'Star' });

    const response = await request(app)
      .post('/api/interact')
      .send({ entityName: 'Galactic Entity', data: [1, 2, 3] });

    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Interaction successful');
    expect(response.body.processedData).toEqual([1, 2, 3]); // Mocked prediction output
  });

  test('should return error for non-existing entity interaction', async () => {
    const response = await request(app)
      .post('/api/interact')
      .send({ entityName: 'Non-Existing Entity', data: [1, 2, 3] });

    expect(response.status).toBe(404);
    expect(response.text).toBe('Entity not found');
  });

  test('should train the model successfully', async () => {
    const response = await request(app)
      .post('/api/train')
      .send({ trainingData: [[1, 2], [3, 4]], labels: [[0], [1]] });

    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Model trained successfully');
  });

  test('should return error for training with invalid data', async () => {
    const response = await request(app)
      .post('/api/train')
      .send({ trainingData: [], labels: [] });

    expect(response.status).toBe(400);
    expect(response.body.errors).toEqual(expect.arrayContaining([
      expect.objectContaining({ msg: 'trainingData must be an array' }),
      expect.objectContaining({ msg: 'labels must be an array' })
    ]));
  });
});
