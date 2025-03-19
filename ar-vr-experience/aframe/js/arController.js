// arController.js

class ARController {
    constructor(scene) {
        this.scene = scene; // Reference to the A-Frame scene
        this.objectToPlace = null; // The object to be placed in AR
        this.isPlacing = false; // Flag to check if we are in placement mode
    }

    // Initialize the AR controller
    init(objectToPlace) {
        this.objectToPlace = objectToPlace;
        this.setupEventListeners();
    }

    // Set up event listeners for touch input
    setupEventListeners() {
        // Listen for touch events
        this.scene.addEventListener('click', (event) => {
            if (this.isPlacing) {
                this.placeObject(event);
            } else {
                this.startPlacement();
            }
        });
    }

    // Start the placement process
    startPlacement() {
        this.isPlacing = true;
        console.log("Tap to place the object.");
    }

    // Place the object in the AR environment
    placeObject(event) {
        const intersection = this.getIntersection(event);
        if (intersection) {
            const { point } = intersection;
            if (!this.objectToPlace.isPlaced) {
                this.objectToPlace.setAttribute('position', `${point.x} ${point.y} ${point.z}`);
                this.objectToPlace.setAttribute('visible', true);
                this.objectToPlace.isPlaced = true; // Mark the object as placed
                console.log("Object placed at:", point);
            } else {
                // Move the object if it is already placed
                this.objectToPlace.setAttribute('position', `${point.x} ${point.y} ${point.z}`);
                console.log("Object moved to:", point);
            }
        }
    }

    // Get the intersection point with the AR plane
    getIntersection(event) {
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        // Convert touch coordinates to normalized device coordinates
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

        // Set the raycaster from the camera to the mouse position
        raycaster.setFromCamera(mouse, this.scene.camera);

        // Check for intersections with AR planes
        const intersects = raycaster.intersectObjects(this.scene.children, true);
        return intersects.length > 0 ? intersects[0] : null;
    }
}

// Example usage
const scene = document.querySelector('a-scene'); // Reference to the A-Frame scene
const objectToPlace = document.createElement('a-entity'); // Create a new entity for the object
objectToPlace.setAttribute('gltf-model', 'url(models/market-item.glb)'); // Set the model
objectToPlace.setAttribute('visible', false); // Initially hidden
objectToPlace.isPlaced = false; // Custom property to track placement

scene.appendChild(objectToPlace); // Add the object to the scene

const arController = new ARController(scene);
arController.init(objectToPlace); // Initialize the AR controller
