// tests/hdgs.test.js

import HyperDimensionalGovernanceSynthesizer from '../../src/governance/hdgs';
import HyperDimensionalTransactionNexus from '../../src/governance/hdgs'; // Assuming HDTN is in this file
import AutonomousGalacticDiplomacyEngine from '../../src/governance/hdgs'; // Assuming AGDE is in this file

jest.mock('../../src/governance/hdgs'); // Mock the HDTN and AGDE classes

describe('HyperDimensionalGovernanceSynthesizer', () => {
    let hdgs;

    beforeEach(() => {
        hdgs = new HyperDimensionalGovernanceSynthesizer();
    });

    test('should propose a valid governance decision', () => {
        const decision = {
            id: 'decision-1',
            details: 'Implement new intergalactic trade regulations.',
            dimensions: ['5D', '6D']
        };
        hdgs.proposeDecision(decision);
        
        expect(hdgs.getProposedDecisions()).toContain(decision);
        expect(hdgs.decisionHistory).toContainEqual(expect.objectContaining({ id: 'decision-1' }));
    });

    test('should throw an error for invalid governance decision', () => {
        const decision = { id: 'decision-2' }; // Missing details and dimensions
        expect(() => hdgs.proposeDecision(decision)).toThrow("Invalid decision proposal.");
    });

    test('should process a governance decision', async () => {
        const decision = {
            id: 'decision-3',
            details: 'Establish a new diplomatic alliance.',
            dimensions: ['5D']
        };
        await hdgs.proposeDecision(decision);
        
        expect(hdgs.hdtn.handleTransaction).toHaveBeenCalledWith(decision);
        expect(hdgs.agde.facilitateDiplomacy).toHaveBeenCalledWith(decision);
    });

    test('should retrieve all proposed decisions', () => {
        const decision1 = {
            id: 'decision-4',
            details: 'Create a new interdimensional currency.',
            dimensions: ['5D', '7D']
        };
        const decision2 = {
            id: 'decision-5',
            details: 'Formulate a new governance structure.',
            dimensions: ['6D']
        };
        hdgs.proposeDecision(decision1);
        hdgs.proposeDecision(decision2);
        
        expect(hdgs.getProposedDecisions()).toEqual([decision1, decision2]);
    });

    test('should retrieve decision history', async () => {
        const decision = {
            id: 'decision-6',
            details: 'Implement a new governance model.',
            dimensions: ['5D']
        };
        await hdgs.proposeDecision(decision);
        
        const history = hdgs.getDecisionHistory();
        expect(history).toContainEqual(expect.objectContaining({ id: 'decision-6' }));
        expect(history[0]).toHaveProperty('timestamp');
    });

    test('should log error for failed decision processing', async () => {
        const decision = {
            id: 'decision-7',
            details: 'Propose a new intergalactic treaty.',
            dimensions: ['5D']
        };
        hdgs.hdtn.handleTransaction.mockRejectedValue(new Error("Transaction failed")); // Simulate failure
        await expect(hdgs.proposeDecision(decision)).rejects.toThrow("Transaction failed");
    });

    test('should clear all proposed decisions', () => {
        const decision = {
            id: 'decision-8',
            details: 'Establish a new trade route.',
            dimensions: ['5D']
        };
        hdgs.proposeDecision(decision);
        expect(hdgs.getProposedDecisions()).toContain(decision);
        
        hdgs.clearDecisions();
        expect(hdgs.getProposedDecisions()).toEqual([]);
    });
});
