// tests/vrController.test.js

const VRController = require('../api/vrController'); // Adjust the path as necessary
const { createScene } = require('./testUtils'); // Utility function to create a mock A-Frame scene

describe('VRController', () => {
    let vrController;
    let scene;

    beforeEach(() => {
        scene = createScene(); // Create a mock A-Frame scene
        vrController = new VRController(scene);
        vrController.init(); // Initialize the VR controller
    });

    test('should select an object on select start', () => {
        const mockObject = document.createElement('a-entity');
        scene.appendChild(mockObject); // Add mock object to the scene

        const mockEvent = { target: vrController.controller1 }; // Mock event with controller
        vrController.onSelectStart(mockEvent);

        expect(vrController.selectedObject).toBe(mockObject);
        expect(mockObject.getAttribute('color')).toBe('green'); // Check color change
    });

    test('should deselect an object on select end', () => {
        const mockObject = document.createElement('a-entity');
        scene.appendChild(mockObject); // Add mock object to the scene

        const mockEvent = { target: vrController.controller1 }; // Mock event with controller
        vrController.onSelectStart(mockEvent); // Select the object
        vrController.onSelectEnd(mockEvent); // Deselect the object

        expect(vrController.selectedObject).toBe(null);
        expect(mockObject.getAttribute('color')).toBe('blue'); // Check color change
    });

    test('should get intersection with VR objects', () => {
        const intersection = vrController.getIntersection(vrController.controller1);
        expect(intersection).toBeDefined();
    });
});
