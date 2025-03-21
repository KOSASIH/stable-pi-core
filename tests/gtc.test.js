const gtc = require('../src/tokens/gtc');
const GalacticWallet = require('../src/tokens/wallet');
const BioQuantumIntegrationLayer = require('../src/tokens/bqil');

jest.mock('../src/tokens/gtc'); // Mock the gtc module
jest.mock('../src/tokens/bqil'); // Mock the BQIL module

describe('GalacticWallet Transfers', () => {
    let wallet1, wallet2;

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
    });

    afterAll(() => {
        jest.clearAllMocks(); // Clear mocks after tests
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
