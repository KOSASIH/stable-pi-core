import VoidHarmonicResonanceNetwork from '../src/quantum/vhrn';

describe('VoidHarmonicResonanceNetwork', () => {
    let vhrn;

    beforeEach(() => {
        vhrn = new VoidHarmonicResonanceNetwork();
    });

    test('should initialize the network', () => {
        vhrn.initializeNetwork();
        expect(vhrn.isActive).toBe(true);
    });

    test('should not initialize the network if already active', () => {
        vhrn.initializeNetwork();
        const consoleSpy = jest.spyOn(console, 'log');
        vhrn.initializeNetwork();
        expect(consoleSpy).toHaveBeenCalledWith("Void Harmonic Resonance Network is already active.");
        consoleSpy.mockRestore();
    });

    test('should stop the network', () => {
        vhrn.initializeNetwork();
        vhrn.stopNetwork();
        expect(vhrn.isActive).toBe(false);
    });

    test('should clear channels and energy levels when stopping the network', () => {
        vhrn.initializeNetwork();
        vhrn.createChannel('Node1');
        vhrn.stopNetwork();
        expect(vhrn.channels).toEqual({});
        expect(vhrn.energyLevels).toEqual({});
    });

    test('should create a communication channel for a node', () => {
        vhrn.initializeNetwork();
        vhrn.createChannel('Node1');
        expect(vhrn.channels).toHaveProperty('Node1');
        expect(vhrn.energyLevels).toHaveProperty('Node1', 100);
    });

    test('should not create a channel if the network is not active', () => {
        const consoleSpy = jest.spyOn(console, 'warn');
        vhrn.createChannel('Node1');
        expect(consoleSpy).toHaveBeenCalledWith("Cannot create channel. The network is not active.");
        consoleSpy.mockRestore();
    });

    test('should send a message to a specific node', async () => {
        vhrn.initializeNetwork();
        vhrn.createChannel('Node1');
        await vhrn.sendMessage('Node1', 'Hello, Node1!');
        expect(vhrn.channels['Node1'].messages).toContain('Hello, Node1!');
    });

    test('should not send a message if the network is not active', async () => {
        const consoleSpy = jest.spyOn(console, 'warn');
        await vhrn.sendMessage('Node1', 'Hello, Node1!');
        expect(consoleSpy).toHaveBeenCalledWith("Cannot send message. The network is not active.");
        consoleSpy.mockRestore();
    });

    test('should not send a message if the channel does not exist', async () => {
        vhrn.initializeNetwork();
        const consoleSpy = jest.spyOn(console, 'warn');
        await vhrn.sendMessage('Node1', 'Hello, Node1!');
        expect(consoleSpy).toHaveBeenCalledWith("No channel exists for node: Node1.");
        consoleSpy.mockRestore();
    });

    test('should transfer energy to a specific node', async () => {
        vhrn.initializeNetwork();
        vhrn.createChannel('Node1');
        await vhrn.transferEnergy('Node1', 50);
        expect(vhrn.energyLevels['Node1']).toBe(50);
    });

    test('should not transfer energy if the network is not active', async () => {
        const consoleSpy = jest.spyOn(console, 'warn');
        await vhrn.transferEnergy('Node1', 50);
        expect(consoleSpy).toHaveBeenCalledWith("Cannot transfer energy. The network is not active.");
        consoleSpy.mockRestore();
    });

    test('should not transfer energy if the channel does not exist', async () => {
        vhrn.initializeNetwork();
        const consoleSpy = jest.spyOn(console, 'warn');
        await vhrn.transferEnergy('Node1', 50);
        expect(consoleSpy).toHaveBeenCalledWith("No channel exists for node: Node1.");
        consoleSpy.mockRestore();
    });

    test('should not transfer energy if insufficient energy is available', async () => {
        vhrn.initializeNetwork();
        vhrn.createChannel('Node1');
        const consoleSpy = jest.spyOn(console, 'warn');
        await vhrn.transferEnergy('Node1', 150); // More than available
        expect(consoleSpy).toHaveBeenCalledWith("Insufficient energy to transfer to Node1. Current energy: 100");
        consoleSpy.mockRestore();
    });

    test('should retrieve messages from a specific node', () => {
        vhrn.initializeNetwork();
        vhrn.createChannel('Node1');
        vhrn.sendMessage('Node1', 'Hello, Node1!');
        const messages = vhrn.retrieveMessages('Node1');
        expect(messages).toContain('Hello, Node1!');
        expect(vhrn.channels['Node1'].messages).toHaveLength(0); // Messages should be cleared after retrieval
    });

    test('should return an empty array if no messages exist for a node', () => {
        vhrn.initializeNetwork();
        vhrn.createChannel('Node1');
        const messages = vhrn.retrieveMessages('Node1');
        expect(messages).toEqual([]);
    });

    test('should log events correctly', () => {
        const message = "Test log message";
        vhrn.logEvent(message);
        expect(vhrn.getLogs()).toContainEqual(expect.stringContaining(message));
    });

    test('should retrieve logs', () => {
        vhrn.logEvent("First log message");
        vhrn.logEvent("Second log message");
        const logs = vhrn.getLogs();
        expect(logs).toHaveLength(2);
        expect(logs[0]).toContain("First log message");
        expect(logs[1]).toContain("Second log message");
    });
});
