// tests/anrf.test.js

const AstroNeuralRealityForge = require('./anrf');

describe('AstroNeuralRealityForge', () => {
    let anrf;

    beforeEach(() => {
        anrf = new AstroNeuralRealityForge();
    });

    test('should create a new virtual reality', () => {
        const reality = anrf.createVirtualReality("Test Reality", { economyType: "barter" });
        expect(reality.name).toBe("Test Reality");
        expect(reality.parameters).toEqual({ economyType: "barter" });
        expect(anrf.virtualRealities.length).toBe(1);
    });

    test('should simulate economy in the virtual reality', () => {
        anrf.createVirtualReality("Test Reality", { economyType: "barter" });
        console.log = jest.fn(); // Mock console.log
        anrf.simulateEconomy("Test Reality");
        expect(console.log).toHaveBeenCalledWith(`Simulating economy in "Test Reality"...`);
    });

    test('should manage governance in the virtual reality', () => {
        anrf.createVirtualReality("Test Reality", { economyType: "barter" });
        console.log = jest.fn(); // Mock console.log
        anrf.manageGovernance("Test Reality", { model: "DAO" });
        expect(console.log).toHaveBeenCalledWith(`Managing governance in "Test Reality" with model:`, { model: "DAO" });
    });

    test('should expand the virtual reality to new dimensions', () => {
        anrf.createVirtualReality("Test Reality", { economyType: "barter" });
        console.log = jest.fn(); // Mock console.log
        anrf.expandToNewDimensions("Test Reality", ["5D", "6D"]);
        expect(console.log).toHaveBeenCalledWith(`Expanding "Test Reality" to new dimensions:`, ["5D", "6D"]);
        expect(anrf.virtualRealities[0].parameters.dimensions).toEqual(["5D", "6D"]);
    });

    test('should list all created virtual realities', () => {
        anrf.createVirtualReality("Test Reality", { economyType: "barter" });
        console.log = jest.fn(); // Mock console.log
        anrf.listVirtualRealities();
        expect(console.log).toHaveBeenCalledWith("Current Virtual Realities:");
        expect(console.log).toHaveBeenCalledWith("- Test Reality (Created at:");
    });

    test('should handle non-existent virtual reality in simulation', () => {
        console.error = jest.fn(); // Mock console.error
        anrf.simulateEconomy("NonExistentReality");
        expect(console.error).toHaveBeenCalledWith(`Virtual reality "NonExistentReality" not found.`);
    });

    test('should handle non-existent virtual reality in governance management', () => {
        console.error = jest.fn(); // Mock console.error
        anrf.manageGovernance("NonExistentReality", { model: "DAO" });
        expect(console.error).toHaveBeenCalledWith(`Virtual reality "NonExistentReality" not found.`);
    });

    test('should handle non-existent virtual reality in expansion', () => {
        console.error = jest.fn(); // Mock console.error
        anrf.expandToNewDimensions("NonExistentReality", ["5D"]);
        expect(console.error).toHaveBeenCalledWith(`Virtual reality "NonExistentReality" not found.`);
    });
});
