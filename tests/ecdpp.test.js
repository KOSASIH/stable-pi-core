// tests/ecdpp.test.js

import ExoCivilizationDiplomacyProtocol from '../src/space/ecdpp';

describe('ExoCivilizationDiplomacyProtocol', () => {
    let ecdp;

    beforeEach(() => {
        ecdp = new ExoCivilizationDiplomacyProtocol();
    });

    test('should initialize ECDP with language algorithms and trade protocols', () => {
        const languageAlgorithms = {
            'CivilizationA': { translate: jest.fn().mockReturnValue('Translated Message') },
        };
        const tradeProtocols = {
            'CivilizationA': { executeTrade: jest.fn().mockReturnValue('Trade Successful') },
        };
        ecdp.initializeECDP(languageAlgorithms, tradeProtocols);
        
        expect(ecdp.languageAlgorithms).toEqual(languageAlgorithms);
        expect(ecdp.tradeProtocols).toEqual(tradeProtocols);
    });

    test('should throw an error if no language algorithm is available for a civilization', () => {
        expect(() => ecdp.communicateWithCivilization('CivilizationB', 'Hello')).toThrow("No language algorithm available for civilization: CivilizationB");
    });

    test('should communicate with an extraterrestrial civilization', () => {
        const languageAlgorithms = {
            'CivilizationA': { translate: jest.fn().mockReturnValue('Translated Message') },
        };
        ecdp.initializeECDP(languageAlgorithms, {});
        
        ecdp.logCommunication = jest.fn(); // Mock logCommunication
        ecdp.communicateWithCivilization('CivilizationA', 'Hello');
        
        expect(languageAlgorithms['CivilizationA'].translate).toHaveBeenCalledWith('Hello');
        expect(ecdp.logCommunication).toHaveBeenCalledWith('CivilizationA', 'Translated Message');
    });

    test('should log communication history', () => {
        const languageAlgorithms = {
            'CivilizationA': { translate: jest.fn().mockReturnValue('Translated Message') },
        };
        ecdp.initializeECDP(languageAlgorithms, {});
        
        ecdp.communicateWithCivilization('CivilizationA', 'Hello');
        expect(ecdp.communicationHistory).toHaveLength(1);
        expect(ecdp.communicationHistory[0]).toEqual(expect.objectContaining({
            civilization: 'CivilizationA',
            message: 'Translated Message',
        }));
    });

    test('should throw an error if no trade protocol is available for a civilization', () => {
        expect(() => ecdp.initiateTrade('CivilizationB', { item: 'Resource' })).toThrow("No trade protocol available for civilization: CivilizationB");
    });

    test('should initiate a trade with an extraterrestrial civilization', () => {
        const tradeProtocols = {
            'CivilizationA': { executeTrade: jest.fn().mockReturnValue('Trade Successful') },
        };
        ecdp.initializeECDP({}, tradeProtocols);
        
        ecdp.logTrade = jest.fn(); // Mock logTrade
        const result = ecdp.initiateTrade('CivilizationA', { item: 'Resource' });
        
        expect(result).toBe('Trade Successful');
        expect(ecdp.logTrade).toHaveBeenCalledWith('CivilizationA', { item: 'Resource' }, 'Trade Successful');
    });

    test('should log trade history', () => {
        const tradeProtocols = {
            'CivilizationA': { executeTrade: jest.fn().mockReturnValue('Trade Successful') },
        };
        ecdp.initializeECDP({}, tradeProtocols);
        
        ecdp.initiateTrade('CivilizationA', { item: 'Resource' });
        expect(ecdp.tradeHistory).toHaveLength(1);
        expect(ecdp.tradeHistory[0]).toEqual(expect.objectContaining({
            civilization: 'CivilizationA',
            tradeDetails: { item: 'Resource' },
            tradeResult: 'Trade Successful',
        }));
    });

    test('should retrieve communication history', () => {
        const languageAlgorithms = {
            'CivilizationA': { translate: jest.fn().mockReturnValue('Translated Message') },
        };
        ecdp.initializeECDP(languageAlgorithms, {});
        
        ecdp.communicateWithCivilization('CivilizationA', 'Hello');
        const history = ecdp.getCommunicationHistory();
        expect(history).toHaveLength(1);
    });

    test('should retrieve trade history', () => {
        const tradeProtocols = {
            'CivilizationA': { executeTrade: jest.fn().mockReturnValue('Trade Successful') },
        };
        ecdp.initializeECDP({}, tradeProtocols);
        
        ecdp.initiateTrade('CivilizationA', { item: 'Resource' });
        const history = ecdp.getTradeHistory();
        expect(history).toHaveLength(1);
    });

    test('should reset the ECDP', () => {
        const languageAlgorithms = {
            'CivilizationA': { translate: jest.fn().mockReturnValue('Translated Message') },
        };
        const tradeProtocols = {
            'CivilizationA': { executeTrade: jest.fn().mockReturnValue('Trade Successful') },
        };
        ecdp.initializeECDP(languageAlgorithms, tradeProtocols);
        ecdp.resetECDP();
        
        expect(ecdp.languageAlgorithms).toEqual({});
        expect(ecdp.tradeProtocols).toEqual({});
        expect(ecdp.communicationHistory).toEqual([]);
        expect(ecdp.tradeHistory).toEqual([]);
    });
});
