// tests/deployGTC.test.js

const gtc = require('../src/tokens/gtc');
const stability = require('../src/tokens/stability');
const GalacticWallet = require('../src/tokens/wallet');
const BioQuantumIntegrationLayer = require('../src/tokens/bqil');
const aies = require('../src/space/aies');
const { deployGTC, transferGTC, sendGU, checkBalances, stabilizeGTC, initializeSRNF } = require('../path/to/deployGTC'); // Adjust the path accordingly

jest.mock('../src/tokens/gtc');
jest.mock('../src/tokens/stability');
jest.mock('../src/tokens/wallet');
jest.mock('../src/tokens/bqil');
jest.mock('../src/space/aies');

describe('GTC Deployment Functions', () => {
    let wallet1, wallet2;

    beforeEach(() => {
        wallet1 = new GalacticWallet("0xUser 1");
        wallet2 = new GalacticWallet("0xUser 2");
    });

    test('should deploy GTC successfully', async () => {
        gtc.initialize.mockResolvedValue();
        BioQuantumIntegrationLayer.addValidBioSignal.mockResolvedValue();
        BioQuantumIntegrationLayer.authenticate.mockResolvedValue();
        gtc.transferGTC.mockResolvedValue();
        stability.getCurrentPriceGTC.mockResolvedValue(314159);
        stability.stabilize.mockResolvedValue();
        aies.initialize.mockResolvedValue();
        aies.evolveInfrastructure.mockResolvedValue();

        await deployGTC();

        expect(gtc.initialize).toHaveBeenCalled();
        expect(BioQuantumIntegrationLayer.addValidBioSignal).toHaveBeenCalled();
        expect(BioQuantumIntegrationLayer.authenticate).toHaveBeenCalled();
        expect(gtc.transferGTC).toHaveBeenCalledTimes(2);
        expect(stability.getCurrentPriceGTC).toHaveBeenCalled();
        expect(stability.stabilize).toHaveBeenCalled();
        expect(aies.initialize).toHaveBeenCalled();
        expect(aies.evolveInfrastructure).toHaveBeenCalled();
    });

    test('should transfer GTC successfully', async () => {
        gtc.transferGTC.mockResolvedValue();

        await transferGTC("ownerAddress", wallet1.address, 1000, 'validBioSignal');

        expect(gtc.transferGTC).toHaveBeenCalledWith("ownerAddress", wallet1.address, 1000, 'validBioSignal');
    });

    test('should send GU successfully', async () => {
        wallet1.sendGU = jest.fn().mockResolvedValue();

        await sendGU(wallet1, wallet2, 1000);

        expect(wallet1.sendGU).toHaveBeenCalledWith(wallet2.address, 1000);
    });

    test('should check balances successfully', async () => {
        wallet1.checkBalance = jest.fn().mockResolvedValue({ GTC: 1000, GU: 500 });
        wallet2.checkBalance = jest.fn().mockResolvedValue({ GTC: 2000, GU: 1000 });

        await checkBalances(wallet1, wallet2);

        expect(wallet1.checkBalance).toHaveBeenCalled();
        expect(wallet2.checkBalance).toHaveBeenCalled();
    });

    test('should stabilize GTC price successfully', async () => {
        stability.getCurrentPriceGTC.mockResolvedValue(314159);
        stability.stabilize.mockResolvedValue();

        await stabilizeGTC();

        expect(stability.getCurrentPriceGTC).toHaveBeenCalled();
        expect(stability.stabilize).toHaveBeenCalledWith(314159);
    });

    test('should initialize and activate SRNF successfully', async () => {
        await initializeSRNF();

        expect(aies.initialize).toHaveBeenCalled();
        expect(aies.evolveInfrastructure).toHaveBeenCalled();
    });
});
