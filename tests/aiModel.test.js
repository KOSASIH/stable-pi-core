// tests/aiModel.test.js - Unit tests for AI Model module

import AIModel from '../src/space/aiModel';
import * as tf from '@tensorflow/tfjs'; // Import TensorFlow.js

jest.mock('@tensorflow/tfjs'); // Mock TensorFlow.js for testing

describe('AIModel', () => {
    let aiModel;
    const modelPath = 'path/to/model.json';

    beforeEach(() => {
        aiModel = new AIModel(modelPath);
    });

    test('should initialize the model', async () => {
        const mockModel = { predict: jest.fn() };
        tf.loadLayersModel.mockResolvedValue(mockModel); // Mock the model loading

        await aiModel.initialize();
        expect(tf.loadLayersModel).toHaveBeenCalledWith(modelPath);
        expect(aiModel.model).toBe(mockModel);
    });

    test('should throw an error if model initialization fails', async () => {
        tf.loadLayersModel.mockRejectedValue(new Error('Failed to load model'));

        await expect(aiModel.initialize()).rejects.toThrow('Failed to initialize AI model');
    });

    test('should preprocess data correctly', () => {
        const inputData = [[1, 2, 3], [4, 5, 6]];
        const expectedTensor = tf.tensor(inputData);

        const tensorData = aiModel.preprocessData(inputData);
        expect(tensorData).toEqual(expectedTensor);
    });

    test('should make predictions', async () => {
        const mockModel = { predict: jest.fn().mockReturnValue(tf.tensor([[0.5]])) };
        aiModel.model = mockModel; // Set the mocked model

        const inputData = [[1, 2, 3]];
        const processedData = aiModel.preprocessData(inputData);
        await aiModel.analyze(inputData);

        expect(mockModel.predict).toHaveBeenCalledWith(processedData);
    });

    test('should throw an error if model is not initialized before prediction', async () => {
        const inputData = [[1, 2, 3]];

        await expect(aiModel.analyze(inputData)).rejects.toThrow('AI model is not initialized');
    });

    test('should throw an error during analysis if prediction fails', async () => {
        const mockModel = { predict: jest.fn().mockImplementation(() => { throw new Error('Prediction error'); }) };
        aiModel.model = mockModel; // Set the mocked model

        const inputData = [[1, 2, 3]];
        await expect(aiModel.analyze(inputData)).rejects.toThrow('Failed to analyze data');
    });
});
