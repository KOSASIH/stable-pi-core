// tests/qnha.test.js
const QuantumNebulaHarvestingArray = require('./qnha');

describe('QuantumNebulaHarvestingArray Tests', () => {
  beforeEach(() => {
    // Reset the instance before each test
    QuantumNebulaHarvestingArray.energyHarvested = 0;
    QuantumNebulaHarvestingArray.nebulaData = {};
  });

  test('should initialize nebula with potential energy', () => {
    QuantumNebulaHarvestingArray.initializeNebula('Nebula Carina', 5);
    expect(QuantumNebulaHarvestingArray.nebulaData['Nebula Carina']).toEqual({
      potentialEnergy: 5,
      harvestedEnergy: 0,
    });
  });

  test('should harvest energy from initialized nebula', async () => {
    QuantumNebulaHarvestingArray.initializeNebula('Nebula Carina', 5);
    const energy = await QuantumNebulaHarvestingArray.harvestFromNebula('Nebula Carina');
    expect(energy).toBe(0.5);
    expect(QuantumNebulaHarvestingArray.getTotalEnergyHarvested()).toBe(0.5);
    expect(QuantumNebulaHarvestingArray.getNebulaHarvestedEnergy('Nebula Carina')).toBe(0.5);
  });

  test('should not harvest more than potential energy', async () => {
    QuantumNebulaHarvestingArray.initializeNebula('Nebula Carina', 0.5);
    await QuantumNebulaHarvestingArray.harvestFromNebula('Nebula Carina');
    const energy = await QuantumNebulaHarvestingArray.harvestFromNebula('Nebula Carina');
    expect(energy).toBe(0);
    expect(QuantumNebulaHarvestingArray.getNebulaHarvestedEnergy('Nebula Carina')).toBe(0.5);
  });

  test('should convert harvested energy to CNC', async () => {
    QuantumNebulaHarvestingArray.initializeNebula('Nebula Carina', 5);
    await QuantumNebulaHarvestingArray.harvestFromNebula('Nebula Carina');
    const cnc = await QuantumNebulaHarvestingArray.convertToCNC(0.5);
    expect(cnc).toBe(5);
  });

  test('should throw error for conversion with zero energy', async () => {
    await expect(QuantumNebulaHarvestingArray.convertToCNC(0)).rejects.toThrow('Energy must be greater than zero for conversion.');
  });

  test('should throw error for uninitialized nebula', async () => {
    await expect(QuantumNebulaHarvestingArray.harvestFromNebula('Nebula Orion')).rejects.toThrow('Nebula Nebula Orion not initialized.');
  });

  test('should automate harvesting and conversion process', async () => {
    QuantumNebulaHarvestingArray.initializeNebula('Nebula Carina', 5);
    const cnc = await QuantumNebulaHarvestingArray.automatedHarvestAndConvert('Nebula Carina');
    expect(cnc).toBe(5);
    expect(QuantumNebulaHarvestingArray.getTotalEnergyHarvested()).toBe(0.5);
  });

  test('should handle multiple nebulae correctly', async () => {
    QuantumNebulaHarvestingArray.initializeNebula('Nebula Carina', 5);
    QuantumNebulaHarvestingArray.initializeNebula('Nebula Orion', 3);
    
    await QuantumNebulaHarvestingArray.automatedHarvestAndConvert('Nebula Carina');
    await QuantumNebulaHarvestingArray.automatedHarvestAndConvert('Nebula Orion');
    
    expect(QuantumNebulaHarvestingArray.getTotalEnergyHarvested()).toBe(1);
    expect(QuantumNebulaHarvestingArray.getNebulaHarvestedEnergy('Nebula Carina')).toBe(0.5);
    expect(QuantumNebulaHarvestingArray.getNebulaHarvestedEnergy('Nebula Orion')).toBe(0.5);
  });
});
