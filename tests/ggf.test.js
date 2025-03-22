// tests/ggf.test.js

import GalacticGovernanceFramework from '../src/space/ggf';

describe('GalacticGovernanceFramework', () => {
    let ggf;

    beforeEach(() => {
        ggf = new GalacticGovernanceFramework();
    });

    test('should register a new entity', () => {
        const entityId = 'PlanetA';
        ggf.registerEntity(entityId);
        expect(ggf.entities.has(entityId)).toBe(true);
    });

    test('should log when an entity is registered', () => {
        const entityId = 'PlanetA';
        const logSpy = jest.spyOn(ggf.logger, 'log');
        ggf.registerEntity(entityId);
        expect(logSpy).toHaveBeenCalledWith(`Entity registered: ${entityId}`);
    });

    test('should not register the same entity twice', () => {
        const entityId = 'PlanetA';
        ggf.registerEntity(entityId);
        const logSpy = jest.spyOn(ggf.logger, 'log');
        ggf.registerEntity(entityId);
        expect(logSpy).toHaveBeenCalledWith(`Entity already registered: ${entityId}`);
    });

    test('should create a new proposal', () => {
        const entityId = 'PlanetA';
        ggf.registerEntity(entityId);
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', entityId);
        expect(proposal).toHaveProperty('id');
        expect(proposal).toHaveProperty('title', 'Establish Trade Routes');
        expect(proposal).toHaveProperty('description', 'Proposal to establish trade routes.');
        expect(proposal).toHaveProperty('proposer', entityId);
    });

    test('should throw an error when an unauthorized entity tries to create a proposal', () => {
        expect(() => {
            ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'UnauthorizedEntity');
        }).toThrow('Unauthorized proposer');
    });

    test('should vote on a proposal', () => {
        const entityIdA = 'PlanetA';
        const entityIdB = 'PlanetB';
        ggf.registerEntity(entityIdA);
        ggf.registerEntity(entityIdB);
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', entityIdA);
        
        ggf.voteOnProposal(proposal.id, entityIdB);
        expect(proposal.votes).toBe(1);
    });

    test('should throw an error when an unauthorized entity tries to vote', () => {
        const entityIdA = 'PlanetA';
        const entityIdB = 'PlanetB';
        ggf.registerEntity(entityIdA);
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', entityIdA);
        
        expect(() => {
            ggf.voteOnProposal(proposal.id, 'UnauthorizedEntity');
        }).toThrow('Unauthorized voter');
    });

    test('should throw an error when voting on a non-existent proposal', () => {
        const entityId = 'PlanetA';
        ggf.registerEntity(entityId);
        
        expect(() => {
            ggf.voteOnProposal('nonExistentProposalId', entityId);
        }).toThrow('Proposal not found');
    });

    test('should throw an error when an entity votes more than once on the same proposal', () => {
        const entityIdA = 'PlanetA';
        const entityIdB = 'PlanetB';
        ggf.registerEntity(entityIdA);
        ggf.registerEntity(entityIdB);
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', entityIdA);
        
        ggf.voteOnProposal(proposal.id, entityIdB);
        expect(() => {
            ggf.voteOnProposal(proposal.id, entityIdB);
        }).toThrow('Entity has already voted on this proposal');
    });

    test('should approve a proposal when it reaches quorum', () => {
        const entityIdA = 'PlanetA';
        const entityIdB = 'PlanetB';
        const entityIdC = 'PlanetC';
        ggf.registerEntity(entityIdA);
        ggf.registerEntity(entityIdB);
        ggf.registerEntity(entityIdC);
        
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', entityIdA);
        ggf.voteOnProposal(proposal.id, entityIdB);
        ggf.voteOnProposal(proposal.id, entityIdC);
        
        expect(proposal.status).toBe('approved');
    });

    test('should execute an approved proposal', () => {
        const entityIdA = 'PlanetA';
        const entityIdB = 'PlanetB';
        const entityIdC = 'PlanetC';
        ggf.registerEntity(entityIdA);
        ggf.registerEntity(entityIdB);
        ggf.registerEntity(entityIdC);
        
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', entityIdA);
        ggf.voteOnProposal(proposal.id, entityIdB);
        ggf.voteOnProposal(proposal.id, entityIdC);
        
        ggf.executeProposal(proposal.id);
        expect(proposal.status).toBe('executed');
    });

    test('should throw an error when executing a non-approved proposal', () => {
        const entityId = 'PlanetA';
        ggf.registerEntity(entityId);
        
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', entityId);
        expect(() => {
            ggf.executeProposal(proposal.id);
        }).toThrow('Proposal must be approved before execution');
    });

    test('should get voting results for a proposal', () => {
        const entityIdA = 'PlanetA';
        const entityIdB = 'PlanetB';
        ggf.registerEntity(entityIdA);
        ggf.registerEntity(entityIdB);
        
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', entityIdA);
        ggf.voteOnProposal(proposal.id, entityIdB);
        
        const results = ggf.getVotingResults(proposal.id);
        expect(results).toHaveProperty('proposalId', proposal.id);
        expect(results).toHaveProperty('votes', 1);
        expect(results).toHaveProperty('status', proposal.status);
    });

    test('should throw an error when getting voting results for a non-existent proposal', () => {
        expect(() => {
            ggf.getVotingResults('nonExistentProposalId');
        }).toThrow('Proposal not found');
    });
});
