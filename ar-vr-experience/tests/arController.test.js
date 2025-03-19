// tests/arController.test.js

const ARController = require('../api/arController'); // Adjust the path as necessary
const { createScene } = require('./testUtils'); // Utility function to create a mock A-Frame scene

describe('ARController', () => {
    let arController;
    let scene;

    beforeEach(() => {
        scene = createScene(); // Create a mock A-Frame scene
        arController = new ARController(scene);
        arController.init(); // Initialize the AR controller
    });

    test('should start placement mode', () => {
        arController.startPlacement();
        expect(arController.isPlacing).toBe(true);
    });

    test('should place object in AR environment', () => {
        const mockObject = document.createElement('a-entity');
        arController.objectToPlace = mockObject;

        const mockEvent = { clientX: 100, clientY: 100 }; // Mock touch event
        arController.placeObject(mockEvent);

        expect(mockObject.getAttribute('position')).toBeDefined();
        expect(mockObject.isPlaced).toBe(true);
    });

    test('should handle intersection correctly', () => {
        const mockEvent = { clientX: 100, clientY: 100 }; // Mock touch event
        const intersection = arController.getIntersection(mockEvent);
        expect(intersection).toBeDefined();
    });
});
