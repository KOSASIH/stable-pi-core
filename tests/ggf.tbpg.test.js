// tests/ggf.tbpg.test.js

import GalacticGovernanceFramework from '../src/space/ggf';
import TachyonBasedPredictiveGovernance from '../src/space/tbpg';

describe('GalacticGovernanceFramework with Tachyon-Based Predictive Governance Integration', () => {
    let ggf;

    beforeEach(() => {
        ggf = new GalacticGovernanceFramework();
    });

    test('should initialize GGF with a tachyonic communication protocol', () => {
        const mockProtocol = {
            sendMessage: jest.fn(),
        };
        ggf.initializeGGF(mockProtocol);
        expect(ggf.tachyonicCommunicationProtocol).toBe(mockProtocol);
    });

    test('should create a prediction model for a scenario', () => {
        const scenario = 'economic_growth';
        const model = (data) => data.growthRate > 2 ? 'Growth' : 'Stagnation';
        
        ggf.tbpg.createPredictionModel(scenario, model);
        expect(ggf.tbpg.predictionModels[scenario]).toBe(model);
    });

    test('should predict future outcomes based on current data', () => {
        const scenario = 'economic_growth';
        const model = (data) => data.growthRate > 2 ? 'Growth' : 'Stagnation';
        ggf.tbpg.createPredictionModel(scenario, model);
        
        const currentData = { growthRate: 3 };
        const prediction = ggf.tbpg.predictFuture(scenario, currentData);
        
        expect(prediction).toHaveProperty('outcome', 'Predicted outcome based on {"growthRate":3} using model function');
        expect(prediction).toHaveProperty('confidence');
    });

    test('should send predictions to relevant nodes', () => {
        const mockProtocol = {
            sendMessage: jest.fn(),
        };
        ggf.initializeGGF(mockProtocol);
        
        const scenario = 'economic_growth';
        const model = (data) => data.growthRate > 2 ? 'Growth' : 'Stagnation';
        ggf.tbpg.createPredictionModel(scenario, model);
        
        const currentData = { growthRate: 3 };
        const predictions = ggf.tbpg.predictFuture(scenario, currentData);
        
        const nodes = ['Node1', 'Node2'];
        ggf.tbpg.sendPredictionsToNodes(predictions, nodes);
        
        nodes.forEach(node => {
            expect(mockProtocol.sendMessage).toHaveBeenCalledWith(node, {
                type: 'prediction',
                predictions,
            });
        });
    });

    test('should throw an error when predicting with a non-existent model', () => {
        const currentData = { growthRate: 3 };
        expect(() => ggf.tbpg.predictFuture('nonExistentScenario', currentData)).toThrow('No prediction model found for scenario: nonExistentScenario');
    });

    test('should create a new proposal', () => {
        const title = 'Establish Trade Routes';
        const description = 'Proposal to establish trade routes between planets.';
        const proposer = 'PlanetA';
        
        const proposal = ggf.createProposal(title, description, proposer);
        expect(proposal).toHaveProperty('id');
        expect(proposal).toHaveProperty('title', title);
        expect(proposal).toHaveProperty('description', description);
        expect(proposal).toHaveProperty('proposer', proposer);
    });

    test('should vote on a proposal', () => {
        const title = 'Establish Trade Routes';
        const description = 'Proposal to establish trade routes between planets.';
        const proposer = 'PlanetA';
        
        const proposal = ggf.createProposal(title, description, proposer);
        ggf.voteOnProposal(proposal.id, 'PlanetB');
        expect(proposal.votes).toBe(1);
    });

    test('should execute a proposal if approved', () => {
        const title = 'Establish Trade Routes';
        const description = 'Proposal to establish trade routes between planets.';
        const proposer = 'PlanetA';
        
        const proposal = ggf.createProposal(title, description, proposer);
        ggf.voteOnProposal(proposal.id, 'PlanetB');
        ggf.voteOnProposal(proposal.id, 'PlanetC');
        ggf.executeProposal(proposal.id);
        expect(proposal.status).toBe('executed');
    });

    test('should throw an error when executing a non-approved proposal', () => {
        const title = 'Establish Trade Routes';
        const description = 'Proposal to establish trade routes between planets.';
        const proposer = 'PlanetA';
        
        const proposal = ggf.createProposal(title, description, proposer);
        expect(() => ggf.executeProposal(proposal.id)).toThrow('Proposal must be approved before execution');
    });
});
