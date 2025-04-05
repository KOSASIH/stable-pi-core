const GalacticGovernanceFramework = require('../../src/space/ggf');
const HyperDimensionalGovernanceSynthesizer = require('../../src/governance/hdgs'); // Import HDGS
const AstroCosmicConsciousnessNetwork = require('../../src/space/accn'); // Import ACCN
const CosmoFractalGovernanceAmplifier = require('../../src/governance/cfga'); // Import CFGA
const OmniSpectralGovernanceMatrix = require('../../src/space/ggf').OmniSpectralGovernanceMatrix; // Import OSGM

jest.mock('../../src/governance/hdgs'); // Mock the HDGS class
jest.mock('../../src/space/accn'); // Mock the ACCN class
jest.mock('../../src/governance/cfga'); // Mock the CFGA class
jest.mock('../../src/space/ggf'); // Mock the OSGM class

describe('GalacticGovernanceFramework', () => {
    let ggf;

    beforeEach(() => {
        ggf = new GalacticGovernanceFramework();
        const mockProtocol = {
            sendMessage: jest.fn((node, message) => {
                console.log(`Message sent to ${node}:`, message);
            })
        };
        ggf.initializeGGF(mockProtocol); // Initialize GGF with a mock protocol
    });

    test('should register a new entity', () => {
        ggf.registerEntity('PlanetA');
        expect(ggf.entities.has('PlanetA')).toBe(true);
    });

    test('should not register the same entity twice', () => {
        ggf.registerEntity('PlanetA');
        ggf.registerEntity('PlanetA'); // Attempt to register again
        expect(ggf.entities.size).toBe(1); // Should still be 1
    });

    test('should create a new proposal', () => {
        ggf.registerEntity('PlanetA');
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        expect(proposal).toHaveProperty('id');
        expect(proposal.title).toBe('Establish Trade Routes');
        expect(ggf.proposals).toContainEqual(proposal);
    });

    test('should throw an error for unauthorized proposer', () => {
        expect(() => {
            ggf.createProposal('Unauthorized Proposal', 'This should fail.', 'PlanetB'); // Not registered
        }).toThrow('Unauthorized proposer');
    });

    test('should allow voting on a proposal', () => {
        ggf.registerEntity('PlanetA');
        ggf.registerEntity('PlanetB');
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        
        ggf.voteOnProposal(proposal.id, 'PlanetB');
        expect(proposal.votes).toBe(1);
        expect(ggf.votes.get(proposal.id).has('PlanetB')).toBe(true);
    });

    test('should throw an error for unauthorized voter', () => {
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        expect(() => {
            ggf.voteOnProposal(proposal.id, 'PlanetC'); // Not registered
        }).toThrow('Unauthorized voter');
    });

    test('should throw an error for already voted entity', () => {
        ggf.registerEntity('PlanetA');
        ggf.registerEntity('PlanetB');
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        
        ggf.voteOnProposal(proposal.id, 'PlanetB');
        expect(() => {
            ggf.voteOnProposal(proposal.id, 'PlanetB'); // Voting again
        }).toThrow('Entity has already voted on this proposal');
    });

    test('should approve a proposal when quorum is reached', () => {
        ggf.registerEntity('PlanetA');
        ggf.registerEntity('PlanetB');
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        
        ggf.voteOnProposal(proposal.id, 'PlanetA'); // Vote from proposer
        ggf.voteOnProposal(proposal.id, 'PlanetB'); // Vote from another entity
        
        expect(proposal.status).toBe('approved');
        expect(HyperDimensionalGovernanceSynthesizer.prototype.proposeDecision).toHaveBeenCalledWith({
            id: proposal.id,
            details: proposal.description,
            dimensions: ['5D', '6D'], // Example dimensions
        });
    });

    test('should get voting results for a proposal', () => {
        ggf.registerEntity('PlanetA');
        ggf.registerEntity('PlanetB');
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        
        ggf.voteOnProposal(proposal.id, 'PlanetB');
        const results = ggf.getVotingResults(proposal.id);
        
        expect(results).toEqual({
            proposalId: proposal.id,
            votes: 1,
            status: 'pending',
        });
    });

    test('should execute an approved proposal', () => {
        ggf.registerEntity('PlanetA');
        ggf.registerEntity('PlanetB');
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        
        ggf.voteOnProposal(proposal.id, 'PlanetA');
        ggf.voteOnProposal(proposal.id, 'PlanetB');
        
        ggf.executeProposal(proposal.id);
        expect(proposal.status).toBe('executed');
    });

    test('should throw an error when executing a non-approved proposal', () => {
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        expect(() => {
            ggf.executeProposal(proposal.id); // Not approved yet
        }).toThrow('Proposal must be approved before execution');
    });

    test('should send proposals to nodes', () => {
        const mockProtocol = {
            sendMessage: jest.fn()
        };
        ggf.tachyonicCommunicationProtocol = mockProtocol; // Set the mock protocol
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        
        ggf.sendProposalsToNodes([proposal], ['Node1', 'Node2']);
        expect(mockProtocol.sendMessage).toHaveBeenCalledTimes(2);
    });

    test('should gather cosmic insights from ACCN', async () => {
        const mockResponse = 'Cosmic alignment is favorable.';
        AstroCosmicConsciousnessNetwork.prototype.communicate.mockResolvedValue(mockResponse); // Mock ACCN response

        const insight = await ggf.gatherCosmicInsights('Pulsar A', 'What is the status of cosmic alignment?');
        expect(insight).toBe(mockResponse);
        expect(AstroCosmicConsciousnessNetwork.prototype.communicate).toHaveBeenCalledWith('Pulsar A', 'What is the status of cosmic alignment?');
    });

    // New tests for CFGA integration
    test('should amplify governance using CFGA', async () => {
        await ggf.amplifyGovernance();
        expect(CosmoFractalGovernanceAmplifier.prototype.amplifyGovernance).toHaveBeenCalled();
    });

    test('should evaluate governance efficiency using CFGA', () => {
        const mockEfficiency = 75; // Mock efficiency value
        CosmoFractalGovernanceAmplifier.prototype.evaluateGovernanceEfficiency.mockReturnValue(mockEfficiency);
        
        const efficiency = ggf.evaluateGovernanceEfficiency();
        expect(efficiency).to be(mockEfficiency);
        expect(CosmoFractalGovernanceAmplifier.prototype.evaluateGovernanceEfficiency).toHaveBeenCalled();
    });

    test('should adjust governance structures using CFGA', () => {
        ggf.adjustGovernanceStructures();
        expect(CosmoFractalGovernanceAmplifier.prototype.adjustGovernanceStructures).toHaveBeenCalled();
    });

    test('should manage voting through OSGM', async () => {
        const proposal = ggf.createProposal('Intergalactic Peace Treaty', 'Proposal for a peace treaty between galaxies.', 'PlanetA');
        ggf.registerEntity('PlanetB');
        await ggf.voteOnProposal(proposal.id, 'PlanetB');
        expect(OmniSpectralGovernanceMatrix.prototype.manageVoting).toHaveBeenCalledWith(proposal);
    });

    test('should throw an error if trying to vote on a non-existent proposal', async () => {
        expect(async () => {
            await ggf.voteOnProposal('non-existent-id', 'PlanetA');
        }).rejects.toThrow('Proposal not found');
    });

    test('should handle multiple votes correctly', async () => {
        ggf.registerEntity('PlanetA');
        ggf.registerEntity('PlanetB');
        const proposal = ggf.createProposal('Establish Trade Routes', 'Proposal to establish trade routes.', 'PlanetA');
        
        await ggf.voteOnProposal(proposal.id, 'PlanetA');
        await ggf.voteOnProposal(proposal.id, 'PlanetB');
        
        expect(proposal.votes).toBe(2);
        expect(proposal.status).toBe('approved');
    });
});
