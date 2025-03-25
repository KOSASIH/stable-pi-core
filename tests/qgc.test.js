import QuantumGravitationalConsensus from './qgc';
import CSRFProtection from './csrf_layer'; // Mock CSRF Protection

jest.mock('./csrf_layer'); // Mock the CSRFProtection module

describe('QuantumGravitationalConsensus CSRF Tests', () => {
    let consensus;

    beforeEach(() => {
        consensus = new QuantumGravitationalConsensus();
    });

    test('should add node with valid CSRF token', () => {
        const node = { name: 'Node1', userId: 'user123' };
        const validCsrfToken = 'valid-token';

        CSRFProtection.prototype.verify_token.mockImplementation(() => {});

        expect(() => {
            consensus.addNode(node, validCsrfToken);
        }).not.toThrow();

        expect(consensus.nodes).toContainEqual(node);
    });

    test('should throw error when adding node with invalid CSRF token', () => {
        const node = { name: 'Node2', userId: 'user123' };
        const invalidCsrfToken = 'invalid-token';

        CSRFProtection.prototype.verify_token.mockImplementation(() => {
            throw new Error('Invalid CSRF token');
        });

        expect(() => {
            consensus.addNode(node, invalidCsrfToken);
        }).toThrow('Invalid CSRF token');

        expect(consensus.nodes).not.toContainEqual(node);
    });

    test('should add parallel universe node with valid CSRF token', () => {
        const parallelNode = { name: 'ParallelNode1', userId: 'user123' };
        const validCsrfToken = 'valid-token';

        CSRFProtection.prototype.verify_token.mockImplementation(() => {});

        expect(() => {
            consensus.addParallelUniverseNode(parallelNode, validCsrfToken);
        }).not.toThrow();

        expect(consensus.parallelUniverses).toContainEqual(parallelNode);
    });

    test('should throw error when adding parallel universe node with invalid CSRF token', () => {
        const parallelNode = { name: 'ParallelNode2', userId: 'user123' };
        const invalidCsrfToken = 'invalid-token';

        CSRFProtection.prototype.verify_token.mockImplementation(() => {
            throw new Error('Invalid CSRF token');
        });

        expect(() => {
            consensus.addParallelUniverseNode(parallelNode, invalidCsrfToken);
        }).toThrow('Invalid CSRF token');

        expect(consensus.parallelUniverses).not.toContainEqual(parallelNode);
    });

    test('should synchronize with parallel universe node with valid CSRF token', async () => {
        const parallelNode = { name: 'ParallelNode3', userId: 'user123' };
        const validCsrfToken = 'valid-token';
        consensus.addParallelUniverseNode(parallelNode, validCsrfToken);

        CSRFProtection.prototype.verify_token.mockImplementation(() => {});

        await expect(consensus.synchronizeWithParallelUniverse(parallelNode.name, validCsrfToken)).resolves.not.toThrow();
    });

    test('should throw error when synchronizing with parallel universe node with invalid CSRF token', async () => {
        const parallelNode = { name: 'ParallelNode4', userId: 'user123' };
        const invalidCsrfToken = 'invalid-token';
        consensus.addParallelUniverseNode(parallelNode, invalidCsrfToken);

        CSRFProtection.prototype.verify_token.mockImplementation(() => {
            throw new Error('Invalid CSRF token');
        });

        await expect(consensus.synchronizeWithParallelUniverse(parallelNode.name, invalidCsrfToken)).rejects.toThrow('Invalid CSRF token');
    });
});
