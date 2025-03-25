import FractalRealitySimulator from '../src/core/frs';

describe('FractalRealitySimulator', () => {
    let frs;

    beforeEach(() => {
        frs = new FractalRealitySimulator();
    });

    test('should initialize FRS with a time dilation compensator', () => {
        const mockTDC = {}; // Mock QuantumTimeDilationCompensator
        frs.initializeFRS(mockTDC);
        expect(frs.timeDilationCompensator).toBe(mockTDC);
    });

    test('should start the simulation', () => {
        frs.startSimulation();
        expect(frs.isActive).toBe(true);
    });

    test('should stop the simulation', () => {
        frs.startSimulation();
        frs.stopSimulation();
        expect(frs.isActive).toBe(false);
    });

    test('should generate fractal data', async () => {
        const mockTDC = {
            calculateAverageOffset: jest.fn().mockReturnValue(0), // Mock method
        };
        frs.initializeFRS(mockTDC);
        await frs.startSimulation();
        const data = await frs.generateFractalData(0);
        expect(data).toHaveProperty('timestamp');
        expect(data).toHaveProperty('fractalPattern');
        expect(data).toHaveProperty('predictions');
        frs.stopSimulation();
    });

    test('should log events correctly', () => {
        const message = "Test log message";
        frs.logEvent(message);
        expect(frs.getLogs()).toContainEqual(expect.stringContaining(message));
    });

    test('should retrieve logs', () => {
        frs.logEvent("First log message");
        frs.logEvent("Second log message");
        const logs = frs.getLogs();
        expect(logs).toHaveLength(2);
        expect(logs[0]).toContain("First log message");
        expect(logs[1]).toContain("Second log message");
    });

    test('should generate predictions based on fractal data', () => {
        const predictions = frs.generatePredictions(0);
        expect(predictions).toHaveProperty('economicForecast');
        expect(predictions).toHaveProperty('governanceInsights');
        expect(predictions).toHaveProperty('intergalacticExpansion');
    });

    test('should handle asynchronous operations correctly', async () => {
        const mockTDC = {
            calculateAverageOffset: jest.fn().mockReturnValue(10), // Mock method
        };
        frs.initializeFRS(mockTDC);
        await frs.startSimulation();
        const data = await frs.generateFractalData(10);
        expect(data.fractalPattern).toContain("Fractal pattern based on time offset: 10");
        frs.stopSimulation();
    });
});
