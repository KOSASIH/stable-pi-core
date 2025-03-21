// tests/qgc.test.js

import QuantumGravitationalConsensus from '../src/core/qgc';

describe('QuantumGravitationalConsensus', () => {
    let qgc;

    beforeEach(() => {
        qgc = new QuantumGravitationalConsensus();
    });

    test('addNode - should add a new node', () => {
        const node = { name: 'Node1' };
        qgc.addNode(node);
        expect(qgc.nodes).toHaveLength(1);
        expect(qgc.nodes[0].name).toBe('Node1');
    });

    test('addNode - should not add duplicate node', () => {
        const node = { name: 'Node1' };
        qgc.addNode(node);
        expect(() => {
            qgc.addNode(node);
        }).toThrow('Node Node1 already exists in the consensus network.');
    });

    test('addParallelUniverseNode - should add a new parallel universe node', () => {
        const node = { name: 'ParallelNode1' };
        qgc.addParallelUniverseNode(node);
        expect(qgc.parallelUniverses).toHaveLength(1);
        expect(qgc.parallelUniverses[0].name).toBe('ParallelNode1');
    });

    test('addParallelUniverseNode - should not add duplicate parallel universe node', () => {
        const node = { name: 'ParallelNode1' };
        qgc.addParallelUniverseNode(node);
        expect(() => {
            qgc.addParallelUniverseNode(node);
        }).toThrow('Parallel universe node ParallelNode1 already exists.');
    });

    test('synchronizeWithParallelUniverse - should synchronize with a parallel universe node', async () => {
        const node = { name: 'ParallelNode1' };
        qgc.addParallelUniverseNode(node);
        await qgc.synchronizeWithParallelUniverse('ParallelNode1');
        expect(qgc.parallelUniverses[0].name).toBe('ParallelNode1');
    });

    test('synchronizeWithParallelUniverse - should throw error for non-existent node', async () => {
        await expect(qgc.synchronizeWithParallelUniverse('NonExistentNode')).rejects.toThrow('Parallel universe node NonExistentNode not found.');
    });

    test('fetchDataFromParallelNode - should fetch data from a parallel universe node', async () => {
        const node = { name: 'ParallelNode1' };
        qgc.addParallelUniverseNode(node);
        const data = await qgc.fetchDataFromParallelNode(node);
        expect(data).toEqual({ data: 'Data from ParallelNode1', timestamp: expect.any(Number) });
    });

    test('updateLocalData - should update local data', () => {
        const data = { data: 'Test data' };
        console.log = jest.fn(); // Mock console.log
        qgc.updateLocalData(data);
        expect(console.log).toHaveBeenCalledWith('Updating local data with: Test data');
    });

    test('handleConsensus - should handle consensus across nodes', async () => {
        const node = { name: 'Node1' };
        qgc.addNode(node);
        console.log = jest.fn(); // Mock console.log
        await qgc.handleConsensus();
        expect(console.log).toHaveBeenCalledWith('Handling consensus across nodes...');
    });

    test('resolveDiscrepancies - should resolve discrepancies', async () => {
        console.log = jest.fn(); // Mock console.log
        await qgc.resolveDiscrepancies();
        expect(console.log).toHaveBeenCalledWith('Discrepancies resolved.');
    });

    test('synchronizeWithAllParallelUniverses - should synchronize with all parallel universe nodes', async () => {
        const node1 = { name: 'ParallelNode1' };
        const node2 = { name: 'ParallelNode2' };
        qgc.addParallelUniverseNode(node1);
        qgc.addParallelUniverseNode(node2);
        console.log = jest.fn(); // Mock console.log
        await qgc.synchronizeWithAllParallelUniverses();
        expect(console.log).toHaveBeenCalledWith('Synchronizing with parallel universe node ParallelNode1...');
        expect(console.log).toHaveBeenCalledWith('Synchronizing with parallel universe node ParallelNode2...');
    });
});
