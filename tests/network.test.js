// tests/network.test.js

import StablePiCoreNetwork from '../src/core/network';
import QuantumConsciousnessConsensus from '../src/core/qcc';

describe('StablePiCoreNetwork', () => {
    let network;

    beforeEach(() => {
        network = new StablePiCoreNetwork();
    });

    test('should initialize the network with quantum entanglement', () => {
        const mockEntanglement = {}; // Mock quantum entanglement object
        network.initializeNetwork(mockEntanglement);
        expect(network.qcc.quantumEntanglement).toBe(mockEntanglement);
    });

    test('should add a node to the network', () => {
        const node = 'Node1';
        network.addNode(node);
        expect(network.nodes.has(node)).toBe(true);
    });

    test('should not add the same node twice', () => {
        const node = 'Node1';
        network.addNode(node);
        const logSpy = jest.spyOn(console, 'log');
        network.addNode(node);
        expect(logSpy).toHaveBeenCalledWith(`Node ${node} is already part of the network.`);
    });

    test('should register a consciousness signal for a node', () => {
        const node = 'Node1';
        const signal = 'Signal1';
        network.addNode(node);
        network.registerConsciousnessSignal(node, signal);
        expect(network.qcc.consciousnessSignals.get(node)).toBe(signal);
    });

    test('should throw an error when registering a signal for a non-existent node', () => {
        const signal = 'Signal1';
        expect(() => {
            network.registerConsciousnessSignal('NonExistentNode', signal);
        }).toThrow('Node NonExistentNode is not part of the network.');
    });

    test('should achieve consensus among nodes', () => {
        const node1 = 'Node1';
        const node2 = 'Node2';
        network.addNode(node1);
        network.addNode(node2);
        network.registerConsciousnessSignal(node1, 'Signal1');
        network.registerConsciousnessSignal(node2, 'Signal1');

        const consensusResult = network.achieveConsensus();
        expect(consensusResult).toBe('Signal1');
    });

    test('should throw an error when achieving consensus with no nodes', () => {
        expect(() => {
            network.achieveConsensus();
        }).toThrow('No nodes in the network to achieve consensus.');
    });

    test('should send consensus results to nodes', () => {
        const node = 'Node1';
        network.addNode(node);
        const logSpy = jest.spyOn(console, 'log');
        const results = 'Consensus Result';
        network.sendConsensusResults(results);
        expect(logSpy).toHaveBeenCalledWith(`Sending consensus results to node ${node}: ${results}`);
    });

    test('should throw an error when sending results with no nodes', () => {
        expect(() => {
            network.sendConsensusResults('Some Result');
        }).toThrow('No nodes in the network to send consensus results.');
    });
});
