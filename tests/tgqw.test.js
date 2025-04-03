// tests/tgqw.test.js

import TransGalacticQuantumWeaver from './tgqw';

describe('TransGalacticQuantumWeaver', () => {
    let tgqw;

    beforeEach(() => {
        tgqw = new TransGalacticQuantumWeaver();
        // Add initial resources to the global resource pool for testing
        tgqw.addResourcesToPool({ energy: 5000, materials: 3000 });
    });

    test('should create a new trans-galactic network', () => {
        const resources = { energy: 1000, materials: 500 };
        const network = tgqw.createNetwork("Andromeda", resources);
        expect(network.galaxyName).toBe("Andromeda");
        expect(network.resources).toEqual({ energy: 1000, materials: 500 });
        expect(tgqw.networks.length).toBe(1);
    });

    test('should allocate resources from the global pool', () => {
        const resources = { energy: 2000, materials: 1000 };
        const network = tgqw.createNetwork("Milky Way", resources);
        expect(tgqw.getResourcePoolState()).toEqual({ energy: 3000, materials: 2000 });
    });

    test('should expand an existing network with additional resources', () => {
        const resources = { energy: 1000, materials: 500 };
        const network = tgqw.createNetwork("Andromeda", resources);
        const additionalResources = { energy: 500, materials: 200 };
        tgqw.expandNetwork(network.id, additionalResources);
        expect(network.resources.energy).toBe(1500);
        expect(network.resources.materials).toBe(700);
    });

    test('should create a new node in the specified network', () => {
        const resources = { energy: 1000, materials: 500 };
        const network = tgqw.createNetwork("Andromeda", resources);
        const nodeData = { type: "sensor", location: "Sector 7" };
        const node = tgqw.createNode(network.id, nodeData);
        expect(node.data).toEqual(nodeData);
        expect(network.nodes.length).toBe(1);
    });

    test('should list all created trans-galactic networks', () => {
        const resources = { energy: 1000, materials: 500 };
        tgqw.createNetwork("Andromeda", resources);
        console.log = jest.fn(); // Mock console.log
        tgqw.listNetworks();
        expect(console.log).toHaveBeenCalledWith("Current Trans-Galactic Networks:");
    });

    test('should destroy a trans-galactic network', () => {
        const resources = { energy: 1000, materials: 500 };
        const network = tgqw.createNetwork("Andromeda", resources);
        const result = tgqw.destroyNetwork(network.id);
        expect(result).toBe(true);
        expect(tgqw.networks.length).toBe(0);
    });

    test('should handle destruction of a non-existent network gracefully', () => {
        const result = tgqw.destroyNetwork("non-existent-id");
        expect(result).toBe(false);
    });

    test('should warn when insufficient resources are available for allocation', () => {
        const resources = { energy: 6000, materials: 4000 }; // Exceeds available resources
        console.warn = jest.fn(); // Mock console.warn
        tgqw.createNetwork("Andromeda", resources);
        expect(console.warn).toHaveBeenCalledWith(expect.stringContaining("Insufficient energy in the resource pool."));
        expect(tgqw.getResourcePoolState()).toEqual({ energy: 5000, materials: 3000 }); // No change in pool
    });

    test('should add resources to the global resource pool', () => {
        tgqw.addResourcesToPool({ energy: 2000, materials: 1000 });
        expect(tgqw.getResourcePoolState()).toEqual({ energy: 7000, materials: 4000 });
    });
});
