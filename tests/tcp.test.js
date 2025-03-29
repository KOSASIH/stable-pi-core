const { PanGalacticResonanceAmplifier, TCP } = require('./tcp'); // Adjust the import based on your module export

describe('PanGalacticResonanceAmplifier', () => {
    let amplifier;

    beforeEach(() => {
        amplifier = new PanGalacticResonanceAmplifier();
    });

    test('should generate harmonic frequencies', () => {
        const expectedFrequencies = [
            1e9, 2e9, 3e9, 4e9, 5e9, 6e9, 7e9, 8e9, 9e9, 10e9
        ];
        expect(amplifier.harmonicFrequencies).toEqual(expectedFrequencies);
    });

    test('should amplify signal correctly', () => {
        const signal = 100;
        const amplifiedSignal = amplifier.amplifySignal(signal);
        expect(amplifiedSignal).toBeGreaterThan(0); // Check if the signal is amplified
    });

    test('should apply harmonic resonance correctly', () => {
        const signal = 100;
        const frequency = 1e9; // 1 GHz
        const result = amplifier.applyHarmonicResonance(signal, frequency);
        expect(result).toBeCloseTo(signal * Math.sin(frequency / 1e9), 5); // Check if the result matches the expected sine calculation
    });
});

describe('TCP', () => {
    let tcp;

    beforeEach(() => {
        tcp = new TCP();
    });

    test('should connect to a given address', async () => {
        const address = 'galactic-network.local';
        const connection = await tcp.connect(address);
        expect(connection).toEqual({ address, status: 'connected' });
    });

    test('should throw error when sending signal without connection', async () => {
        await expect(tcp.send(100)).rejects.toThrow('No active connection. Please connect first.');
    });

    test('should send an amplified signal', async () => {
        await tcp.connect('galactic-network.local');
        const signal = 100;
        const amplifiedSignal = await tcp.send(signal);
        expect(amplifiedSignal).toBeGreaterThan(0); // Check if the signal is sent and amplified
    });

    test('should capture and analyze the sent signal using TERA', async () => {
        await tcp.connect('galactic-network.local');
        const signal = 100;
        await tcp.send(signal);
        const insights = await tcp.tera.analyzeEcho(); // Analyze echoes after sending
        expect(insights).toHaveLength(1); // Check if insights are generated
        expect(insights[0]).toHaveProperty('signal', signal); // Check if the signal matches
    });

    test('should throw error when receiving signal without connection', async () => {
        await expect(tcp.receive()).rejects.toThrow('No active connection. Please connect first.');
    });

    test('should receive a signal', async () => {
        await tcp.connect('galactic-network.local');
        const receivedSignal = await tcp.receive();
        expect(receivedSignal).toBeGreaterThan(0); // Check if a signal is received
    });

    test('should capture and analyze the received signal using TERA', async () => {
        await tcp.connect('galactic-network.local');
        const receivedSignal = await tcp.receive();
        const insights = await tcp.tera.analyzeEcho(); // Analyze echoes after receiving
        expect(insights).toHaveLength(1); // Check if insights are generated
        expect(insights[0]).toHaveProperty('signal', receivedSignal); // Check if the signal matches
    });

    test('should close the connection', async () => {
        await tcp.connect('galactic-network.local');
        await tcp.close();
        expect(tcp.connection).toBeNull(); // Check if the connection is closed
    });

    test('should not throw error when closing without connection', async () => {
        await expect(tcp.close()).resolves.not.toThrow();
    });
});
