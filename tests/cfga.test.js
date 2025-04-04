// tests/cfga.test.js

const CosmoFractalGovernanceAmplifier = require('../src/governance/cfga');

describe('CosmoFractalGovernanceAmplifier', () => {
    let cfga;

    beforeEach(() => {
        cfga = new CosmoFractalGovernanceAmplifier();
    });

    test('should amplify governance and create governance structures', async () => {
        await cfga.amplifyGovernance();
        expect(cfga.getGovernanceStructures()).toHaveLength(1); // Check if one governance structure is created
    });

    test('should amplify governance multiple times', async () => {
        await cfga.amplifyGovernance();
        await cfga.amplifyGovernance();
        expect(cfga.getGovernanceStructures()).toHaveLength(2); // Check if two governance structures are created
    });

    test('should evaluate governance efficiency correctly', async () => {
        await cfga.amplifyGovernance();
        const efficiency = cfga.evaluateGovernanceEfficiency();
        expect(efficiency).toBeGreaterThan(0); // Check if efficiency is calculated
        expect(efficiency).toBeLessThanOrEqual(100); // Efficiency should not exceed 100%
    });

    test('should adjust governance structures correctly', async () => {
        await cfga.amplifyGovernance();
        const initialStructures = cfga.getGovernanceStructures();
        cfga.adjustGovernanceStructures();
        const adjustedStructures = cfga.getGovernanceStructures();

        expect(adjustedStructures).not.toEqual(initialStructures); // Check if structures have been adjusted
        adjustedStructures.forEach((structure, index) => {
            expect(structure.complexity).not.toEqual(initialStructures[index].complexity); // Check complexity adjustment
            expect(structure.efficiency).not.toEqual(initialStructures[index].efficiency); // Check efficiency adjustment
        });
    });

    test('should log an error if amplification fails', async () => {
        // Mock the simulateFractalPatterns method to throw an error
        jest.spyOn(cfga.frs, 'simulateFractalPatterns').mockImplementation(() => {
            throw new Error('Fractal simulation failed');
        });

        console.error = jest.fn(); // Mock console.error
        await cfga.amplifyGovernance(); // Attempt to amplify governance
        expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Error amplifying governance: Fractal simulation failed'));
    });

    test('should return 0 efficiency if no governance structures exist', () => {
        const efficiency = cfga.evaluateGovernanceEfficiency();
        expect(efficiency).toBe(0); // Check if efficiency is 0 when no structures exist
    });
});
