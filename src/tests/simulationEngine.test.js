// src/tests/simulationEngine.test.js
const fs = require('fs');
const { createSimulation, getSimulationResults, getAllSimulations } = require('./simulationEngine');

jest.mock('fs'); // Mock the fs module to avoid actual file system operations

describe('Simulation Engine', () => {
  beforeEach(() => {
    // Clear the simulations object before each test
    jest.clearAllMocks();
  });

  test('should create a simulation and log the event', async () => {
    const strategy = 'Test Strategy';
    const simulationId = await createSimulation(strategy);

    expect(simulationId).toMatch(/^sim-[a-z0-9]{9}$/); // Check if the ID is in the correct format
    expect(fs.appendFileSync).toHaveBeenCalledWith(expect.any(String), expect.stringContaining(`Starting simulation: ${simulationId} with strategy: ${strategy}`));
    expect(fs.appendFileSync).toHaveBeenCalledWith(expect.any(String), expect.stringContaining(`Simulation completed: ${simulationId}`));
  });

  test('should retrieve simulation results', async () => {
    const strategy = 'Test Strategy';
    const simulationId = await createSimulation(strategy);
    const results = await getSimulationResults(simulationId);

    expect(results).toHaveProperty('strategy', strategy);
    expect(results).toHaveProperty('results');
    expect(results).toHaveProperty('status', 'completed');
    expect(results).toHaveProperty('duration');
    expect(results).toHaveProperty('createdAt');
  });

  test('should throw an error for non-existing simulation', async () => {
    await expect(getSimulationResults('non-existing-id')).rejects.toThrow('Simulation not found');
  });

  test('should get all simulations', async () => {
    const strategy1 = 'Test Strategy 1';
    const strategy2 = 'Test Strategy 2';
    await createSimulation(strategy1);
    await createSimulation(strategy2);

    const allSimulations = getAllSimulations();
    expect(allSimulations).toHaveLength(2);
    expect(allSimulations[0]).toHaveProperty('strategy', strategy1);
    expect(allSimulations[1]).toHaveProperty('strategy', strategy2);
  });

  test('should log an error if simulation fails', async () => {
    // Override the simulateStrategy function to throw an error
    const originalSimulateStrategy = global.simulateStrategy;
    global.simulateStrategy = jest.fn().mockRejectedValue(new Error('Simulation error'));

    const strategy = 'Failing Strategy';
    const simulationId = await createSimulation(strategy);

    expect(fs.appendFileSync).toHaveBeenCalledWith(expect.any(String), expect.stringContaining(`Simulation failed: ${simulationId} - Error: Simulation error`));

    // Restore the original function
    global.simulateStrategy = originalSimulateStrategy;
  });
});
