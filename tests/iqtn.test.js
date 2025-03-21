// tests/iqtn.test.js

import InterstellarQuantumTeleportationNetwork from '../src/space/iqtn';
import HolographicQuantumLedger from '../src/core/hql';
import { generateQuantumHash } from '../src/core/utils';

jest.mock('../src/core/hql'); // Mock the Holographic Quantum Ledger module

describe('InterstellarQuantumTeleportationNetwork', () => {
    let iqtn;

    beforeEach(() => {
        iqtn = new InterstellarQuantumTeleportationNetwork();
    });

    test('should teleport data successfully', async () => {
        const data = { message: 'Hello, Universe!' };
        const destination = 'Alpha Centauri';
        const transactionHash = await iqtn.teleportData(data, destination);
        
        expect(transactionHash).toBe(generateQuantumHash(data)); // Check if the hash matches
        expect(iqtn.getTeleportationLog()).toHaveLength(1); // Check if the log has the teleportation event
    });

    test('should throw error for invalid destination', async () => {
        const data = { message: 'Hello, Universe!' };
        const invalidDestination = ''; // Invalid destination

        await expect(iqtn.teleportData(data, invalidDestination)).rejects.toThrow("Invalid destination for teleportation.");
    });

    test('should teleport a transaction successfully', async () => {
        const data = { amount: 100 };
        const user = '0xUser 1';
        const transaction = HolographicQuantumLedger.createTransaction(data, user); // Create a transaction
        HolographicQuantumLedger.getTransaction.mockReturnValue(transaction); // Mock the transaction retrieval

        const destination = 'Proxima Centauri';
        const transactionHash = await iqtn.teleportTransaction(transaction.id, destination);
        
        expect(transactionHash).toBe(generateQuantumHash(transaction)); // Check if the hash matches
    });

    test('should throw error when teleporting a non-existent transaction', async () => {
        const invalidTransactionId = 'non-existent-id';
        const destination = 'Sirius';

        await expect(iqtn.teleportTransaction(invalidTransactionId, destination)).rejects.toThrow("Transaction not found.");
    });

    test('should log teleportation events', async () => {
        const data = { message: 'Hello, Universe!' };
        const destination = 'Alpha Centauri';
        await iqtn.teleportData(data, destination);

        const log = iqtn.getTeleportationLog();
        expect(log).toHaveLength(1);
        expect(log[0]).toEqual(expect.objectContaining({
            data,
            destination,
            transactionHash: expect.any(String),
            timestamp: expect.any(Number),
        }));
    });

    test('should set and get maximum teleportation distance', () => {
        iqtn.setMaxTeleportationDistance(5000000);
        expect(iqtn.getMaxTeleportationDistance()).toBe(5000000);
    });

    test('should throw error when setting invalid maximum teleportation distance', () => {
        expect(() => iqtn.setMaxTeleportationDistance(-100)).toThrow("Distance must be greater than zero.");
    });
});
