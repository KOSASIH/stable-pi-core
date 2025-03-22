// tests/tbpg.test.js

import TachyonBasedPredictiveGovernance from '../src/space/tbpg';

describe('TachyonBasedPredictiveGovernance', () => {
    let tbpg;

    beforeEach(() => {
        tbpg = new TachyonBasedPredictiveGovernance();
    });

    test('should initialize with a tachyonic communication protocol', () => {
        const mockProtocol = {
            sendMessage: jest.fn(),
        };
        tbpg.initializeTBPG(mockProtocol);
        expect(tbpg.tachyonicCommunicationProtocol).toBe(mockProtocol);
    });

    test('should create a prediction model for a scenario', () => {
        const scenario = 'economic_growth';
        const model = (data) => data.growthRate > 2 ? 'Growth' : 'Stagnation';
        
        tbpg.createPredictionModel(scenario, model);
        expect(tbpg.predictionModels[scenario]).toBe(model);
    });

    test('should throw an error when creating a model for an existing scenario', () => {
        const scenario = 'economic_growth';
        const model = (data) => data.growthRate > 2 ? 'Growth' : 'Stagnation';
        
        tbpg.createPredictionModel(scenario, model);
        expect(() => tbpg.createPredictionModel(scenario, model)).toThrow(`Prediction model for scenario "${scenario}" already exists.`);
    });

    test('should predict future outcomes based on current data', () => {
        const scenario = 'economic_growth';
        const model = (data) => data.growthRate > 2 ? 'Growth' : 'Stagnation';
        tbpg.createPredictionModel(scenario, model);
        
        const currentData = { growthRate: 3 };
        const prediction = tbpg.predictFuture(scenario, currentData);
        
        expect(prediction).toHaveProperty('outcome', 'Predicted outcome based on {"growthRate":3} using model function');
        expect(prediction).toHaveProperty('confidence');
    });

    test('should throw an error when predicting with a non-existent model', () => {
        const currentData = { growthRate: 3 };
        expect(() => tbpg.predictFuture('nonExistentScenario', currentData)).toThrow('No prediction model found for scenario: nonExistentScenario');
    });

    test('should send predictions to relevant nodes', () => {
        const mockProtocol = {
            sendMessage: jest.fn(),
        };
        tbpg.initializeTBPG(mockProtocol);
        
        const scenario = 'economic_growth';
        const model = (data) => data.growthRate > 2 ? 'Growth' : 'Stagnation';
        tbpg.createPredictionModel(scenario, model);
        
        const currentData = { growthRate: 3 };
        const predictions = tbpg.predictFuture(scenario, currentData);
        
        const nodes = ['Node1', 'Node2'];
        tbpg.sendPredictionsToNodes(predictions, nodes);
        
        nodes.forEach(node => {
            expect(mockProtocol.sendMessage).toHaveBeenCalledWith(node, {
                type: 'prediction',
                predictions,
            });
        });
    });

    test('should throw an error when sending predictions if the protocol is not initialized', () => {
        const predictions = { outcome: 'Growth', confidence: 0.9 };
        expect(() => tbpg.sendPredictionsToNodes(predictions, ['Node1'])).toThrow("Tachyonic communication protocol is not initialized.");
    });

    test('should evaluate the effectiveness of predictions', () => {
        const predictions = { outcome: 'Growth', confidence: 0.9 };
        const actualOutcomes = 'Growth';
        
        const accuracy = tbpg.evaluatePredictions(predictions, actualOutcomes);
        expect(accuracy).toBe(1); // Since the predicted outcome matches the actual outcome
    });

    test('should reset all prediction models', () => {
        const scenario = 'economic_growth';
        const model = (data) => data.growthRate > 2 ?'Growth' : 'Stagnation';
        tbpg.createPredictionModel(scenario, model);
        
        tbpg.resetModels();
        expect(tbpg.predictionModels).toEqual({});
    });
}); 
