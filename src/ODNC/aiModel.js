// src/ODNC/aiModel.js
const tf = require('@tensorflow/tfjs'); // Import TensorFlow.js
const mongoose = require('mongoose');
const EnergyData = require('./models/EnergyData'); // Import the EnergyData model

// Load a pre-trained model or define a new model
let model;

// Function to load or create a model
const loadModel = async () => {
  try {
    model = await tf.loadLayersModel('file://path/to/your/model.json'); // Load a pre-trained model
    console.log('Model loaded successfully');
  } catch (error) {
    console.error('Error loading model:', error);
    throw new Error('Model loading failed');
  }
};

// Function to preprocess energy data
const preprocessData = (energyData) => {
  // Convert energy data to tensors
  const inputs = energyData.map(data => [data.amount]); // Example: using only amount for prediction
  return tf.tensor2d(inputs);
};

// Function to predict resource extraction
const predictResourceExtraction = async (energyData) => {
  if (!model) {
    await loadModel(); // Load the model if not already loaded
  }

  try {
    const inputTensor = preprocessData(energyData);
    const predictions = model.predict(inputTensor).arraySync(); // Get predictions as an array

    return energyData.map((data, index) => ({
      type: data.type,
      predictedValue: predictions[index][0], // Assuming the model outputs a single value
    }));
  } catch (error) {
    console.error('Prediction error:', error);
    throw new Error('Prediction failed');
  }
};

module.exports = { predictResourceExtraction };
