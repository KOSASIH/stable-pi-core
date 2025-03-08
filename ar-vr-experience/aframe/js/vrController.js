// vrController.js

class VRController {
    constructor(scene) {
        this.scene = scene; // Reference to the A-Frame scene
        this.controller1 = null; // Reference to the first VR controller
        this.controller2 = null; // Reference to the second VR controller
        this.selectedObject = null; // Currently selected object
    }

    // Initialize the VR controller
    init() {
        this.setupControllers();
        this.setupEventListeners();
    }

    // Set up VR controllers
    setupControllers() {
        this.controller1 = this.scene.querySelector('#left-controller');
        this.controller2 = this.scene.querySelector('#right-controller');
    }

    // Set up event listeners for controller input
    setupEventListeners() {
        this.controller1.addEventListener('selectstart', (event) => this.onSelectStart(event));
        this.controller1.addEventListener('selectend', (event) => this.onSelectEnd(event));
        this.controller2.addEventListener('selectstart', (event) => this.onSelectStart(event));
        this.controller2.addEventListener('selectend', (event) => this.onSelectEnd(event));
    }

    // Handle the start of selection
    onSelectStart(event) {
        const controller = event.target;
        const intersection = this.getIntersection(controller);
        if (intersection) {
            this.selectedObject = intersection.object; // Select the intersected object
            this.selectedObject.setAttribute('color', 'green'); // Change color to indicate selection
            console.log("Selected object:", this.selectedObject);
        }
    }

    // Handle the end of selection
    onSelectEnd(event) {
        if (this.selectedObject) {
            this.selectedObject.setAttribute('color', 'blue'); // Change color back to indicate deselection
            console.log("Deselected object:", this.selectedObject);
            this.selectedObject = null; // Clear the selected object
        }
    }

    // Get the intersection point with VR objects
    getIntersection(controller) {
        const raycaster = new THREE.Raycaster();
        const tempMatrix = new THREE.Matrix4();
        const controllerPosition = controller.object3D.position;

        // Update the raycaster with the controller's position and direction
        tempMatrix.identity().extractRotation(controller.object3D.matrixWorld);
        raycaster.ray.origin.setFromMatrixPosition(controller.object3D.matrixWorld);
        raycaster.ray.direction.set(0, 0, -1).applyMatrix4(tempMatrix);

        // Check for intersections with objects in the scene
        const intersects = raycaster.intersectObjects(this.scene.children, true);
        return intersects.length > 0 ? intersects[0] : null;
    }
}

// Example usage
const scene = document.querySelector('a-scene'); // Reference to the A-Frame scene
const vrController = new VRController(scene);
vrController.init(); // Initialize the VR controller
