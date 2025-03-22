// tests/qcc.test.js

import QuantumConsciousnessConsensus from '../src/core/qcc';

describe('QuantumConsciousnessConsensus', () => {
    let qcc;

    beforeEach(() => {
        qcc = new QuantumConsciousnessConsensus();
    });

    test('should initialize QCC with quantum entanglement', () => {
        const mockEntanglement = {}; // Mock quantum entanglement object
        qcc.initializeQCC(mockEntanglement);
        expect(qcc.quantumEntanglement).toBe(mockEntanglement);
    });

    test('should add a node to the QCC network', () => {
        const node = 'Node1';
        qcc.addNode(node);
        expect(qcc.nodes.has(node)).toBe(true);
    });

    test('should not add the same node twice', () => {
        const node = 'Node1';
        qcc.addNode(node);
        const logSpy = jest.spyOn(console, 'log');
        qcc.addNode(node);
        expect(logSpy).toHaveBeenCalledWith(`Node ${node} is already part of the network.`);
    });

    test('should register a consciousness signal for a node', () => {
        const node = 'Node1';
        const signal = 'Signal1';
        qcc.addNode(node);
        qcc.registerConsciousnessSignal(node, signal);
        expect(qcc.consciousnessSignals.get(node)).toBe(signal);
    });

    test('should throw an error when registering a signal for a non-existent node', () => {
        const signal = 'Signal1';
        expect(() => {
            qcc.registerConsciousnessSignal('NonExistentNode', signal);
        }).toThrow('Node NonExistentNode is not part of the network.');
    });

    test('should achieve consensus among nodes', () => {
        const node1 = 'Node1';
        const node2 = 'Node2';
        qcc.addNode(node1);
        qcc.addNode(node2);
        qcc.registerConsciousnessSignal(node1, 'Signal1');
        qcc.registerConsciousnessSignal(node2, 'Signal1');

        const consensusResult = qcc.achieveConsensus();
        expect(consensusResult).toBe('Signal1');
    });

    test('should throw an error when achieving consensus with no nodes', () => {
        expect(() => {
            qcc.achieveConsensus();
        }).toThrow('No nodes in the network to achieve consensus.');
    });

    test('should send consensus results to nodes', () => {
        const node = 'Node1';
        qcc.addNode(node);
        const logSpy = jest.spyOn(console, 'log');
        const results = 'Consensus Result';
        qcc.sendConsensusResults(results);
        expect(logSpy).toHaveBeenCalledWith(`Sending consensus results to node ${node}: ${results}`);
    });

    test('should throw an error when sending results with no nodes', () => {
        expect(() => {
            qcc.sendConsensusResults('Some Result');
        }).toThrow('No nodes in the network to send consensus results.');
    });
});
