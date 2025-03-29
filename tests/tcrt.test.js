// tests/tcrt.test.js

import TransCosmicResonanceTransducer from '../src/core/tcrt';

describe('TransCosmicResonanceTransducer', () => {
    let tcrt;

    beforeEach(() => {
        tcrt = new TransCosmicResonanceTransducer();
    });

    test('should initialize with empty transmissions and parallel universes', () => {
        expect(tcrt.getAllTransmissions()).toEqual([]);
        expect(tcrt.getParallelUniverses()).toEqual([]);
    });

    test('should add a parallel universe', () => {
        const universeId = 'universe-1';
        tcrt.addParallelUniverse(universeId);
        expect(tcrt.getParallelUniverses()).toContain(universeId);
    });

    test('should not add the same parallel universe twice', () => {
        const universeId = 'universe-1';
        tcrt.addParallelUniverse(universeId);
        tcrt.addParallelUniverse(universeId); // Attempt to add again
        expect(tcrt.getParallelUniverses()).toEqual([universeId]);
    });

    test('should initiate communication with a parallel universe', async () => {
        const universeId = 'universe-1';
        const message = 'Hello, Universe!';
        tcrt.addParallelUniverse(universeId);

        const response = await tcrt.initiateCommunication(universeId, message);
        expect(response).toBe(`Response from ${universeId}: Acknowledged`);
        expect(tcrt.getAllTransmissions()).toHaveLength(1);
        expect(tcrt.getAllTransmissions()[0]).toMatchObject({
            universeId,
            message,
            timestamp: expect.any(Number),
        });
    });

    test('should handle communication failure', async () => {
        const universeId = 'universe-2';
        const message = 'Hello, Universe!';
        tcrt.addParallelUniverse(universeId);

        // Mock the sendMessageToUniverse method to simulate failure
        jest.spyOn(tcrt, 'sendMessageToUniverse').mockImplementation(() => {
            return Promise.reject(new Error('Failed to communicate'));
        });

        await expect(tcrt.initiateCommunication(universeId, message)).rejects.toThrow('Failed to communicate');
        expect(tcrt.getAllTransmissions()).toHaveLength(1); // Transmission should still be recorded
    });

    test('should clear all transmissions', () => {
        const universeId = 'universe-1';
        const message = 'Hello, Universe!';
        tcrt.addParallelUniverse(universeId);
        tcrt.initiateCommunication(universeId, message);

        expect(tcrt.getAllTransmissions()).toHaveLength(1);
        tcrt.clearTransmissions();
        expect(tcrt.getAllTransmissions()).toEqual([]);
    });
});
