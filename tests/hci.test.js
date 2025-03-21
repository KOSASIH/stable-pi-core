// tests/hci.test.js

import HolographicConsciousnessInterface from '../src/tokens/hci';

describe('HolographicConsciousnessInterface', () => {
    let hci;

    beforeEach(() => {
        hci = new HolographicConsciousnessInterface();
    });

    test('should initialize the interface with a user consciousness', () => {
        const user = 'User1';
        hci.initializeInterface(user);
        expect(hci.userConsciousness).toBe(user);
        expect(hci.virtualEnvironment).toEqual(expect.objectContaining({
            elements: [],
            interactions: [],
            settings: expect.any(Object),
        }));
    });

    test('should throw an error if no user consciousness is provided during initialization', () => {
        expect(() => hci.initializeInterface(null)).toThrow("User  consciousness must be provided.");
    });

    test('should create a virtual environment', () => {
        hci.initializeInterface('User1');
        expect(hci.virtualEnvironment).toHaveProperty('elements');
        expect(hci.virtualEnvironment).toHaveProperty('interactions');
        expect(hci.virtualEnvironment).toHaveProperty('settings');
    });

    test('should add an element to the virtual environment', () => {
        hci.initializeInterface('User1');
        const element = { name: 'Cube' };
        hci.addElementToEnvironment(element);
        expect(hci.virtualEnvironment.elements).toContainEqual(expect.objectContaining({ name: 'Cube' }));
    });

    test('should throw an error when adding an invalid element', () => {
        expect(() => hci.addElementToEnvironment({})).toThrow("Element must have a valid name.");
    });

    test('should interact with an element in the virtual environment', () => {
        hci.initializeInterface('User1');
        const element = { name: 'Sphere' };
        hci.addElementToEnvironment(element);
        const action = { type: 'manipulate' };
        hci.interactWithElement(0, action); // Interact with the first element
        expect(hci.interactionHistory).toHaveLength(1);
        expect(hci.interactionHistory[0]).toEqual(expect.objectContaining({ elementId: 0, action }));
    });

    test('should throw an error when interacting with a non-existent element', () => {
        expect(() => hci.interactWithElement(999, { type: 'observe' })).toThrow("Element not found in the virtual environment.");
    });

    test('should perform actions on elements correctly', () => {
        hci.initializeInterface('User1');
        const element = { name: 'Pyramid' };
        hci.addElementToEnvironment(element);
        const action = { type: 'observe' };
        const consoleLogSpy = jest.spyOn(console, 'log');
        hci.interactWithElement(0, action);
        expect(consoleLogSpy).toHaveBeenCalledWith(`Observing element: Pyramid`);
        consoleLogSpy.mockRestore();
    });

    test('should retrieve interaction history', () => {
        hci.initializeInterface('User1');
        const element = { name: 'Cylinder' };
        hci.addElementToEnvironment(element);
        hci.interactWithElement(0, { type: 'manipulate' });
        const history = hci.getInteractionHistory();
        expect(history).toHaveLength(1);
        expect(history[0]).toEqual(expect.objectContaining({ elementId: 0 }));
    });

    test('should reset the interface', () => {
        hci.initializeInterface('User1');
        hci.resetInterface();
        expect(hci.userConsciousness).toBeNull();
        expect(hci.virtualEnvironment).toEqual(expect.objectContaining({
            elements: [],
            interactions: [],
            settings: expect.any(Object),
        }));
        expect(hci.interactionHistory).toEqual([]);
    });

    test('should adjust environment settings', () => {
        hci.initializeInterface('User1');
        const newSettings = { lighting: 'dim', gravity: 'low' };
        hci.adjustEnvironmentSettings(newSettings);
        expect(hci.virtualEnvironment.settings).toEqual(expect.objectContaining(newSettings));
    });

    test('should throw an error when simulating consciousness transfer without new consciousness', () => {
        expect(() => hci.simulateConsciousnessTransfer(null)).toThrow("New consciousness must be provided for transfer.");
    });

    test('should simulate consciousness transfer', () => {
        hci.initializeInterface('User1');
        hci.simulateConsciousnessTransfer('User2');
        expect(hci.userConsciousness).toBe('User2');
    });
});
