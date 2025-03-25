const InterplanetaryTransactionProtocol = require('../src/space/itp');
const axios = require('axios');

jest.mock('axios'); // Mock axios for HTTP requests

describe('InterplanetaryTransactionProtocol', () => {
    let itp;

    beforeEach(() => {
        itp = new InterplanetaryTransactionProtocol();
    });

    test('should create a new transaction', () => {
        const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100, { condition: 'ifPlanetBIsReady' });
        expect(transaction).toHaveProperty('id');
        expect(transaction.sender).toBe('PlanetA');
        expect(transaction.receiver).toBe('PlanetB');
        expect(transaction.amount).toBe(100);
        expect(transaction.conditions).toEqual({ condition: 'ifPlanetBIsReady' });
        expect(transaction.status).toBe('pending');
        expect(itp.transactions).toContainEqual(transaction);
    });

    test('should throw an error for invalid transaction amount', () => {
        expect(() => {
            itp.createTransaction('PlanetA', 'PlanetB', -50);
        }).toThrow('Transaction amount must be greater than zero.');
    });

    test('should validate a valid transaction', () => {
        const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100);
        expect(itp.validateTransaction(transaction)).toBe(true);
    });

    test('should invalidate a transaction with incorrect hash', () => {
        const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100);
        transaction.hash = 'invalidhash';
        expect(itp.validateTransaction(transaction)).toBe(false);
    });

    test('should broadcast transaction to peers', async () => {
        itp.addPeer('http://node1.example.com');
        const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100);
        axios.post.mockResolvedValue({ status: 200 }); // Mock successful response

        await itp.broadcastTransaction(transaction);
        expect(axios.post).toHaveBeenCalledWith('http://node1.example.com/transactions', transaction);
    });

    test('should handle incoming transaction', async () => {
        const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100);
        await itp.handleIncomingTransaction(transaction);
        expect(itp.transactions).toContainEqual(transaction);
    });

    test('should log invalid transaction when handling', async () => {
        const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100);
        transaction.hash = 'invalidhash'; // Make it invalid
        await itp.handleIncomingTransaction(transaction);
        expect(itp.transactions).not.toContainEqual(transaction);
    });

    test('should add transaction to blockchain', async () => {
        const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100);
        await itp.handleIncomingTransaction(transaction);
        expect(itp.blockchain).toContainEqual(transaction);
    });

    test('should add a peer node', () => {
        itp.addPeer('http://node1.example.com');
        expect(itp.peers).toContain('http://node1.example.com');
    });

    test('should remove a peer node', () => {
        itp.addPeer('http://node1.example.com');
        itp.removePeer('http://node1.example.com');
        expect(itp.peers).not.toContain('http://node1.example.com');
    });

    test('should get all transactions', () => {
        const transaction1 = itp.createTransaction('PlanetA', 'PlanetB', 100);
        const transaction2 = itp.createTransaction('PlanetC', 'PlanetD', 200);
        expect(itp.getAllTransactions()).toEqual([transaction1, transaction2]);
    });

    test('should get blockchain', async () => {
        const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100);
        await itp.handleIncomingTransaction(transaction);
        expect(itp.getBlockchain()).toContainEqual(transaction);
    });

    // EMQS Tests
    test('should absorb external technology', () => {
        const alienTechnology = {
            name: 'Alien Tech 1',
            protocols: {
                communication: 'Quantum Entanglement Protocol',
                dataTransfer: 'Hyperlight Data Stream'
            }
        };

        itp.absorbExternalTechnology(alienTechnology);
        expect(itp.listIntegratedTechnologies()).toContainEqual(alienTechnology);
    });

    test('should not absorb the same technology twice', () => const alienTechnology = {
            name: 'Alien Tech 1',
            protocols: {
                communication: 'Quantum Entanglement Protocol',
                dataTransfer: 'Hyperlight Data Stream'
            }
        };

        itp.absorbExternalTechnology(alienTechnology);
        itp.absorbExternalTechnology(alienTechnology); // Attempt to absorb again
        expect(itp.listIntegratedTechnologies()).toHaveLength(1); // Should still be one
    });

    test('should list all integrated technologies', () => {
        const alienTechnology1 = {
            name: 'Alien Tech 1',
            protocols: {
                communication: 'Quantum Entanglement Protocol',
                dataTransfer: 'Hyperlight Data Stream'
            }
        };
        const alienTechnology2 = {
            name: 'Alien Tech 2',
            protocols: {
                communication: 'Dimensional Wave Protocol',
                dataTransfer: 'Subspace Data Stream'
            }
        };

        itp.absorbExternalTechnology(alienTechnology1);
        itp.absorbExternalTechnology(alienTechnology2);
        expect(itp.listIntegratedTechnologies()).toEqual([alienTechnology1, alienTechnology2]);
    });

    test('should remove an integrated technology', () => {
        const alienTechnology = {
            name: 'Alien Tech 1',
            protocols: {
                communication: 'Quantum Entanglement Protocol',
                dataTransfer: 'Hyperlight Data Stream'
            }
        };

        itp.absorbExternalTechnology(alienTechnology);
        itp.emqs.removeTechnology('Alien Tech 1');
        expect(itp.listIntegratedTechnologies()).not.toContainEqual(alienTechnology);
    });

    test('should not remove a non-existent technology', () => {
        const consoleSpy = jest.spyOn(console, 'warn').mockImplementation(); // Spy on console.warn
        itp.emqs.removeTechnology('NonExistentTech');
        expect(consoleSpy).toHaveBeenCalledWith('Technology NonExistentTech not found in integrated technologies.');
        consoleSpy.mockRestore(); // Restore original console.warn
    });
});
