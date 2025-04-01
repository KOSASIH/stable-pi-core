const gtc = require('../src/tokens/gtc');
const GalacticWallet = require('../src/tokens/wallet');
const BioQuantumIntegrationLayer = require('../src/tokens/bqil');
const GalacticGovernanceFramework = require('../src/space/ggf');
const AutonomousThreatNeutralizationMatrix = require('../src/core/atnm');

jest.mock('../src/tokens/gtc'); // Mock the gtc module
jest.mock('../src/tokens/bqil'); // Mock the BQIL module
jest.mock('../src/space/ggf'); // Mock the GGF module
jest.mock('../src/core/atnm'); // Mock the ATNM module

describe('Large Scale Testing of Autonomous Features', () => {
    let wallet1, wallet2, ggf, atnm;

    beforeAll(async () => {
        await gtc.initialize();
        wallet1 = new GalacticWallet("0xTest1");
        wallet2 = new GalacticWallet("0xTest2");

        // Mock initial balances
        gtc.getBalance.mockImplementation((address) => {
            if (address === wallet1.address) {
                return { GTC: 100, GU: 0 }; // Initial balance for wallet1
            } else if (address === wallet2.address) {
                return { GTC: 0, GU: 0 }; // Initial balance for wallet2
            }
            return { GTC: 0, GU: 0 }; // Default case
        });

        // Mock BQIL behavior
        BioQuantumIntegrationLayer.addValidBioSignal.mockImplementation(() => Promise.resolve());
        BioQuantumIntegrationLayer.authenticate.mockImplementation(() => Promise.resolve());

        // Initialize Galactic Governance Framework
        ggf = new GalacticGovernanceFramework();
        const mockProtocol = {
            sendMessage: (node, message) => {
                console.log(`Message sent to ${node}:`, message);
            }
        };
        ggf.initializeGGF(mockProtocol);

        // Initialize Autonomous Threat Neutralization Matrix
        atnm = new AutonomousThreatNeutralizationMatrix();
        atnm.initialize();
    });

    afterAll(() => {
        jest.clearAllMocks(); // Clear mocks after tests
    });

    test('Terrestrial Economic Crisis Simulation', async () => {
        console.log('Simulating Terrestrial Economic Crisis...');
        
        // Create a proposal for economic recovery
        const proposal = ggf.createProposal('Economic Recovery Plan', 'Proposal to stabilize the economy during the crisis.', 'PlanetA');
        
        // Simulate voting
        await ggf.voteOnProposal(proposal.id, 'PlanetB');
        await ggf.voteOnProposal(proposal.id, 'PlanetC');

        // Check voting results
        const results = ggf.getVotingResults(proposal.id);
        expect(results.status).toBe('approved');

        // Execute the proposal
        await ggf.executeProposal(proposal.id);
        expect(proposal.status).toBe('executed');
    });

    test('Intergalactic Trade with Martian Colony', async () => {
        console.log('Simulating Intergalactic Trade with Martian Colony...');
        
        // Register entities
        ggf.registerEntity('Earth');
        ggf.registerEntity('Mars Colony');

        // Create a trade proposal
        const tradeProposal = ggf.createProposal('Trade Agreement with Mars', 'Proposal to establish trade routes with Mars Colony.', 'Earth');
        
        // Simulate voting on the trade proposal
        await ggf.voteOnProposal(tradeProposal.id, 'Mars Colony');
        
        // Check voting results
        const tradeResults = ggf.getVotingResults(tradeProposal.id);
        expect(tradeResults.status).toBe('approved');

        // Execute the trade proposal
        await ggf.executeProposal(tradeProposal.id);
        expect(tradeProposal.status).toBe('executed');
    });

    test('Cosmic Threat Response (Supernova)', async () => {
        console.log('Simulating Cosmic Threat: Supernova...');
        
        // Simulate detection of a cosmic threat
        const threat = await atnm.detectThreat();
        expect(threat).toBeTruthy();

        // Handle the detected threat
        await atnm.handleThreat(threat);
        
        // Check if the threat was neutralized
        expect(threat.status).toBe('neutralized');
    });

    test('GTC transfer works with valid bio-signal', async () => {
        const bioSignal = 'validBioSignal'; // Simulated bio-signal
        await BioQuantumIntegrationLayer.addValidBioSignal(bioSignal);
        await BioQuantumIntegrationLayer.authenticate(bioSignal);

        await gtc.transferGTC(gtc.owner, wallet1.address, 100, bioSignal); // 100 GTC
        await wallet1.sendGTC(wallet2.address, 10, bioSignal); // Send 10 GTC

        const balance1 = await wallet1.checkBalance();
        const balance2 = await wallet2.checkBalance();

        expect(balance1.GTC).toBe(90); // 100 - 10 GTC
        expect(balance2.GTC).toBe(10); // 10 GTC received
    });

    test('GU transfer works with valid bio-signal', async () => {
        const bioSignal = 'validBioSignal'; // Simulated bio-signal
        await BioQuantumIntegrationLayer.addValidBioSignal(bioSignal);
        await BioQuantumIntegrationLayer.authenticate(bioSignal);

        await wallet1.sendGU(wallet2.address, 31415.9); // 31415.9 GU = $31,415.9

        const balance1 = await wallet1.checkBalance();
        const balance2 = await wallet2.checkBalance();

        expect(balance1.GU).toBe(31415.9); // 31415.9 GU sent
        expect(balance2.GU).toBe(31415.9); // 31415.9 GU received
    });

    test('Insufficient GTC balance throws error', async () => {
        await expect(wallet1.sendGTC(wallet2.address, 200, 'validBioSignal')).rejects.toThrow('Insufficient GTC balance');
    });

    test('Insufficient GU balance throws error', async () => {
        await expect(wallet1.sendGU(wallet2.address, 50000)).rejects.toThrow('Insufficient GU balance');
    });

    test('Transaction history is updated correctly', async () => {
        const bioSignal = 'validBioSignal'; // Simulated bio-signal
        await BioQuantumIntegrationLayer.addValidBioSignal(bioSignal);
        await BioQuantumIntegrationLayer.authenticate(bioSignal);

        await wallet1.sendGTC(wallet2.address, 5, bioSignal); // Send 5 GTC
        const history = wallet1.getTransactionHistory();

        expect(history).toHaveLength(1);
        expect(history[0]).toEqual(expect.objectContaining({
            type: 'GTC',
            to: wallet2.address,
            amount: 5,
        }));
    });

    test('Invalid bio-signal throws error during transfer', async () => {
        const invalidBioSignal = 'invalidBioSignal'; // Simulated invalid bio-signal
        await expect(wallet1.sendGTC(wallet2.address, 10, invalidBioSignal)).rejects.toThrow('Bio-signal authentication failed.');
    });
});
