// src/ODNC/server.js
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose');
const rateLimit = require('express-rate-limit');
const { predictResourceExtraction } = require('./aiModel'); // Placeholder for AI model
require('dotenv').config(); // Load environment variables

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Rate limiting middleware
const limiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later.',
});
app.use(limiter);

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err));

// Energy data schema
const energyDataSchema = new mongoose.Schema({
  energyType: String,
  amount: Number,
  convertedAmount: Number,
  createdAt: { type: Date, default: Date.now },
});

const EnergyData = mongoose.model('EnergyData', energyDataSchema);

// Endpoint to identify and convert energy
app.post('/api/convert-energy', async (req, res) => {
  const { energyType, amount } = req.body;
  const conversionResult = convertEnergy(energyType, amount);
  
  if (conversionResult) {
    // Save to database
    const energyEntry = new EnergyData({ energyType, amount, convertedAmount: conversionResult });
    await energyEntry.save();
    
    res.json({ success: true, result: conversionResult });
  } else {
    res.status(400).json({ success: false, message: 'Invalid energy type or conversion failed.' });
  }
});

// Function to convert energy types
const convertEnergy = (energyType, amount) => {
  // Example conversion logic
  const conversionRates = {
    'dimensional': 1.5,
    'quantum': 2.0,
    'dark': 0.5,
  };

  if (conversionRates[energyType]) {
    return amount * conversionRates[energyType];
  }
  return null;
};

// Endpoint to predict resource extraction
app.post('/api/predict-extraction', async (req, res) => {
  const { energyData } = req.body;
  try {
    const prediction = await predictResourceExtraction(energyData);
    res.json({ success: true, prediction });
  } catch (error) {
    console.error('Prediction error:', error);
    res.status(500).json({ success: false, message: 'Prediction failed.' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
