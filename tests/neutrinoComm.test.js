// tests/neutrinoComm.test.js

import NeutrinoBasedCommunicationArray from '../src/space/neutrinoComm';

describe('NeutrinoBasedCommunicationArray', () => {
    let neutrinoComm;

    beforeEach(() => {
        neutrinoComm = new NeutrinoBasedCommunicationArray();
    });

    test('addNode - should add a new node', () => {
        neutrinoComm.addNode({ name: 'Node1' });
        expect(neutrinoComm.nodes).toHaveLength(1);
        expect(neutrinoComm.nodes[0].name).toBe('Node1');
    });

    test('addNode - should not add duplicate node', () => {
        neutrinoComm.addNode({ name: 'Node1' });
        expect(() => {
            neutrinoComm.addNode({ name: 'Node1' });
        }).toThrow('Node Node1 already exists in the communication array.');
    });

    test('sendMessage - should send a message to a node', async () => {
        neutrinoComm.addNode({ name: 'Node1' });
        await neutrinoComm.sendMessage('Node1', 'Hello, Node1!');
        expect(neutrinoComm.messageQueue).toHaveLength(1);
        expect(neutrinoComm.messageQueue[0]).toEqual({ nodeName: 'Node1', message: 'Hello, Node1!' });
    });

    test('sendMessage - should return error for non-existent node', async () => {
        await expect(neutrinoComm.sendMessage('Node2', 'Hello, Node2!')).rejects.toThrow('Node Node2 not found in the communication array.');
    });

    test('simulateTransmission - should simulate message transmission', async () => {
        jest.useFakeTimers();
        neutrinoComm.addNode({ name: 'Node1' });
        const message = 'Test message';
        const promise = neutrinoComm.sendMessage('Node1', message);

        // Fast-forward time
        jest.advanceTimersByTime(1000); // Simulate 1 second of transmission time

        await promise; // Wait for the promise to resolve
        expect(neutrinoComm.messageQueue).toHaveLength(1);
        expect(neutrinoComm.messageQueue[0]).toEqual({ nodeName: 'Node1', message });
        jest.useRealTimers();
    });

    test('calculateTransmissionTime - should calculate transmission time based on distance', () => {
        neutrinoComm.addNode({ name: 'Node1' });
        const distance = neutrinoComm.getDistanceToNode({ name: 'Node1' });
        const time = neutrinoComm.calculateTransmissionTime({ name: 'Node1' });
        expect(time).toBeCloseTo(distance / 299792458); // Speed of light in m/s
    });

    test('getDistanceToNode - should return distance for a specific node', () => {
        neutrinoComm.addNode({ name: 'Node1' });
        const distance = neutrinoComm.getDistanceToNode({ name: 'Node1' });
        expect(distance).toBeGreaterThan(0); // Assuming distance is defined for Node1
    });

    test('getDistanceToNode - should return 0 for non-existent node', () => {
        const distance = neutrinoComm.getDistanceToNode({ name: 'Node2' });
        expect(distance).toBe(0); // Node2 does not exist
    });

    test('getMessageQueue - should return the current message queue', () => {
        neutrinoComm.addNode({ name: 'Node1' });
        neutrinoComm.sendMessage('Node1', 'Test message');
        const queue = neutrinoComm.getMessageQueue();
        expect(queue).toHaveLength(1);
        expect(queue[0]).toEqual({ nodeName: 'Node1', message: 'Test message' });
    });

    test('clearMessageQueue - should clear the message queue', () => {
        neutrinoComm.addNode({ name: 'Node1' });
        neutrinoComm.sendMessage('Node1', 'Test message');
        neutrinoComm.clearMessageQueue();
        expect(neutrinoComm.messageQueue).toHaveLength(0);
    });
});
