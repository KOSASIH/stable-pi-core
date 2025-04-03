// tests/srnf.test.js

const SelfReplicatingNodeFabricator = require('../../src/space/srnf');
const { aies } = require('../../src/space/aies'); // Mock AIES
const { hql } = require('../../src/core/hql'); // Mock HQL
const { eqfc } = require('../../src/space/eqfc'); // Mock EQFC
const CosmoQuantumMorphicAdaptor = require('../../src/space/cqma'); // Import CQMA

jest.mock('../../src/space/aies'); // Mock the AIES module
jest.mock('../../src/core/hql'); // Mock the HQL module
jest.mock('../../src/space/eqfc'); // Mock the EQFC module
jest.mock('../../src/space/cqma'); // Mock the CQMA class

describe('SelfReplicatingNodeFabricator', () => {
    let srnf;

    beforeEach(() => {
        srnf = new SelfReplicatingNodeFabricator();
        srnf.activate(); // Activate SRNF for testing
    });

    afterEach(() => {
        srnf.deactivate(); // Deactivate SRNF after each test
    });

    test('should activate the SRNF', () => {
        expect(srnf.active).toBe(true);
    });

    test('should load the replication blueprint', async () => {
        await srnf.loadBlueprint();
        expect(hql.getData).toHaveBeenCalledWith('node-replication-blueprint');
        expect(srnf.replicationBlueprint).toEqual({
            cpu: 'quantum-processor',
            comm: 'tachyon-antenna',
            storage: 'holographic-ledger',
            energy: 'quantum-flux-capacitor'
        });
    });

    test('should harvest local resources', async () => {
        const resources = await srnf.harvestLocalResources('Mars Surface');
        expect(Object.keys(resources)).toEqual(expect.arrayContaining(srnf.resourceTypes));
        expect(resources).toHaveProperty('silicon');
        expect(resources).toHaveProperty('iron');
        expect(resources).toHaveProperty('hydrogen');
        expect(resources).toHaveProperty('rare-earths');
    });

    test('should replicate a node if resources are sufficient', async () => {
        eqfc.getEnergyStatus.mockResolvedValue(1000); // Mock energy availability
        const resources = { silicon: 500, iron: 500, hydrogen: 500, 'rare-earths': 500 };
        srnf.harvestLocalResources = jest.fn().mockResolvedValue(resources); // Mock resource harvesting

        const result = await srnf.replicateNode('Mars Surface');
        expect(result).toBe(true);
        expect(aies.registerNewNode).toHaveBeenCalled();
        expect(hql.storeData).toHaveBeenCalled();
    });

    test('should not replicate a node if resources are insufficient', async () => {
        eqfc.getEnergyStatus.mockResolvedValue(1000); // Mock energy availability
        const resources = { silicon: 200, iron: 200, hydrogen: 200, 'rare-earths': 200 };
        srnf.harvestLocalResources = jest.fn().mockResolvedValue(resources); // Mock resource harvesting

        const result = await srnf.replicateNode('Mars Surface');
        expect(result).toBe(false);
        expect(aies.registerNewNode).not.toHaveBeenCalled();
        expect(hql.storeData).not.toHaveBeenCalled();
    });

    test('should not replicate a node if energy is insufficient', async () => {
        eqfc.getEnergyStatus.mockResolvedValue(50); // Mock insufficient energy
        const resources = { silicon: 500, iron: 500, hydrogen: 500, 'rare-earths': 500 };
        srnf.harvestLocalResources = jest.fn().mockResolvedValue(resources); // Mock resource harvesting

        const result = await srnf.replicateNode('Mars Surface');
        expect(result).toBe(false);
        expect(aies.registerNewNode).not.toHaveBeenCalled();
        expect(hql.storeData).not.toHaveBeenCalled();
    });

    test('should determine the current environment based on location', () => {
        const environment = srnf.determineCurrentEnvironment('Mars Surface');
        expect(environment).toEqual({
            type: 'nebula',
            conditions: { density: 0.1, gasComposition: 'carbon-dioxide' }
        });
    });

    test('should deactivate the SRNF', () => {
        srnf.deactivate();
        expect(srnf.active).toBe(false);
    });

    test('should update configuration', () => {
        const newConfig = { resourceThreshold: 2000, energyConsumptionPerNode: 150 };
        srnf.updateConfiguration(newConfig);
        expect(srnf.resourceThreshold).toBe(2000);
        expect(srnf.energyConsumptionPerNode).toBe(150);
    });
});
