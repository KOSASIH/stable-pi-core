import QuantumTimeDilationCompensator from '../src/core/qtdc';

describe('QuantumTimeDilationCompensator', () => {
    let qtdc;

    beforeEach(() => {
        qtdc = new QuantumTimeDilationCompensator();
    });

    test('should initialize QTDC with entangled nodes', () => {
        const nodes = ['Node1', 'Node2', 'Node3'];
        qtdc.initializeQTDC(nodes, null);
        expect(qtdc.entangledNodes).toEqual(nodes);
        expect(qtdc.timeOffsets).toEqual({ Node1: 0, Node2: 0, Node3: 0 });
    });

    test('should adjust time offset for a specific node', () => {
        const nodes = ['Node1'];
        qtdc.initializeQTDC(nodes, null);
        qtdc.adjustTimeOffset('Node1', 5);
        expect(qtdc.getTimeOffset('Node1')).toBe(5);
    });

    test('should throw an error when adjusting time offset for a non-existent node', () => {
        expect(() => qtdc.adjustTimeOffset('Node2', 5)).toThrow("Node Node2 is not part of the entangled nodes.");
    });

    test('should synchronize time across all entangled nodes', async () => {
        const nodes = ['Node1', 'Node2', 'Node3'];
        qtdc.initializeQTDC(nodes, null);
        qtdc.adjustTimeOffset('Node1', 5);
        qtdc.adjustTimeOffset('Node2', -5);
        await qtdc.synchronizeTime();
        expect(qtdc.getTimeOffset('Node1')).toBe(0);
        expect(qtdc.getTimeOffset('Node2')).toBe(0);
        expect(qtdc.getTimeOffset('Node3')).toBe(0);
    });

    test('should calculate the average time offset correctly', () => {
        const nodes = ['Node1', 'Node2', 'Node3'];
        qtdc.initializeQTDC(nodes, null);
        qtdc.adjustTimeOffset('Node1', 10);
        qtdc.adjustTimeOffset('Node2', 0);
        qtdc.adjustTimeOffset('Node3', -10);
        expect(qtdc.calculateAverageOffset()).toBe(0);
    });

    test('should retrieve the current time offset for a specific node', () => {
        const nodes = ['Node1'];
        qtdc.initializeQTDC(nodes, null);
        qtdc.adjustTimeOffset('Node1', 7);
        expect(qtdc.getTimeOffset('Node1')).toBe(7);
    });

    test('should throw an error when retrieving time offset for a non-existent node', () => {
        expect(() => qtdc.getTimeOffset('Node2')).toThrow("Node Node2 is not part of the entangled nodes.");
    });

    test('should reset time offsets for all nodes', () => {
        const nodes = ['Node1', 'Node2'];
        qtdc.initializeQTDC(nodes, null);
        qtdc.adjustTimeOffset('Node1', 5);
        qtdc.adjustTimeOffset('Node2', -3);
        qtdc.resetTimeOffsets();
        expect(qtdc.getTimeOffset('Node1')).toBe(0);
        expect(qtdc.getTimeOffset('Node2')).toBe(0);
    });

    test('should notify nodes of synchronization using tachyonic communication', async () => {
        const nodes = ['Node1', 'Node2'];
        const mockTachyonicProtocol = {
            sendMessage: jest.fn(),
        };
        qtdc.initializeQTDC(nodes, mockTachyonicProtocol);
        await qtdc.synchronizeTime();
        expect(mockTachyonicProtocol.sendMessage).toHaveBeenCalledTimes(2);
        expect(mockTachyonicProtocol.sendMessage).toHaveBeenCalledWith('Node1', expect.objectContaining({
            type: 'synchronization',
            timeOffsets: qtdc.timeOffsets,
        }));
        expect(mockTachyonicProtocol.sendMessage).toHaveBeenCalledWith('Node2', expect.objectContaining({
            type: 'synchronization',
            timeOffsets: qtdc.timeOffsets,
        }));
    });

    test('should warn if no tachyonic communication protocol is initialized', async () => {
        const nodes = ['Node1'];
        qtdc.initializeQTDC(nodes, null);
        console.warn = jest.fn(); // Mock console.warn
        await qtdc.synchronizeTime();
        expect(console.warn).toHaveBeenCalledWith("No tachyonic communication protocol initialized.");
    });

    test('should process events with the Omni-Temporal Causality Shield', () => {
        const event1 = { id: 1, timestamp: Date.now(), data: "First event" };
        const event2 = { id: 2, timestamp: Date.now() + 1000, data: "Second event" };
        const event3 = { id: 3, timestamp: Date.now() - 1000, data: "Invalid event" }; // Causality violation

        expect(qtdc.processEvent(event1)).toBe(true); // Should process successfully
        expect(qtdc.processEvent(event2)).toBe(true); // Should process successfully
        expect(qtdc.processEvent(event3)).toBe(false); // Should fail due to causality violation
    });
});
