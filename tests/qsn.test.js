const qsn = require('../src/core/qsn'); // Adjust the path as necessary
const { srnf } = require('../space/srnf'); // Mocking the SRNF module
const { tcp } = require('../quantum/tcp'); // Mocking the TCP module

jest.mock('../space/srnf');
jest.mock('../quantum/tcp');

describe('Quantum Singularity Nexus', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('should activate the nexus', () => {
        qsn.activate();
        expect(qsn.active).toBe(true);
    });

    test('should connect nodes and send pings', async () => {
        srnf.getNodes.mockResolvedValue([{ id: 'Node1' }, { id: 'Node2' }]);
        
        await qsn.connectNodes();
        
        expect(qsn.connectedNodes.size).toBe(2);
        expect(qsn.connectedNodes.has('Node1')).toBe(true);
        expect(qsn.connectedNodes.has('Node2')).toBe(true);
    });

    test('should send pings to connected nodes', async () => {
        srnf.getNodes.mockResolvedValue([{ id: 'Node1' }, { id: 'Node2' }]);
        await qsn.connectNodes();

        await qsn.connectNodes(); // This will start the pinging process

        // Simulate waiting for the ping to be sent
        await new Promise(resolve => setTimeout(resolve, 31000)); // Wait for 31 seconds

        expect(tcp.send).toHaveBeenCalledWith({
            event: "NEXUS_PING",
            nodes: Array.from(qsn.connectedNodes)
        });
    });

    test('should transfer GU between nodes', async () => {
        srnf.getNodes.mockResolvedValue([{ id: 'Node1' }, { id: 'Node2' }]);
        await qsn.connectNodes();

        const result = await qsn.transferViaNexus('Node1', 'Node2', 100);
        expect(result).toBe(true);
    });

    test('should throw an error when transferring between unconnected nodes', async () => {
        await expect(qsn.transferViaNexus('Node1', 'Node2', 100)).rejects.toThrow("Nodes not connected to Nexus");
    });

    test('should deactivate the nexus', () => {
        qsn.deactivate();
        expect(qsn.active).toBe(false);
    });
});
