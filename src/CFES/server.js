// src/CFES/server.js
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose');
const rateLimit = require('express-rate-limit');
const { generateFractal, evolveFractal } = require('./fractalAlgorithm'); // Fractal algorithms
require('dotenv').config();

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

// User feedback schema
const feedbackSchema = new mongoose.Schema({
  fractalId: String,
  userFeedback: String,
  createdAt: { type: Date, default: Date.now },
});

const Feedback = mongoose.model('Feedback', feedbackSchema);

// Endpoint to generate a new fractal
app.post('/api/generate-fractal', (req, res) => {
  try {
    const fractal = generateFractal();
    res.json({ success: true, fractal });
  } catch (error) {
    console.error('Fractal generation error:', error);
    res.status(500).json({ success: false, message: 'Fractal generation failed.' });
  }
});

// Endpoint to evolve a fractal based on user feedback
app.post('/api/evolve-fractal', async (req, res) => {
  const { fractalId, userFeedback } = req.body;
  try {
    const evolvedFractal = evolveFractal(fractalId, userFeedback);
    // Save feedback to the database
    const feedbackEntry = new Feedback({ fractalId, userFeedback });
    await feedbackEntry.save();
    res.json({ success: true, evolvedFractal });
  } catch (error) {
    console.error('Evolution error:', error);
    res.status(500).json({ success: false, message: 'Fractal evolution failed.' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
