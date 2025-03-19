using System.Collections;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;
using UnityEngine.UI;

public class ARController : MonoBehaviour
{
    [Header("AR Components")]
    [SerializeField] private ARSessionOrigin arSessionOrigin; // Reference to the AR Session Origin
    [SerializeField] private ARRaycastManager arRaycastManager; // Raycast manager for detecting surfaces
    [SerializeField] private GameObject objectToPlace; // Prefab of the object to place in AR
    [SerializeField] private Text placementStatusText; // UI Text to show placement status

    private GameObject spawnedObject; // The currently spawned object
    private bool isPlacing = false; // Flag to check if we are in placement mode

    void Update()
    {
        // Check for touch input
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);

            if (touch.phase == TouchPhase.Began)
            {
                if (isPlacing)
                {
                    PlaceObject(touch);
                }
                else
                {
                    StartPlacement();
                }
            }
        }
    }

    // Start the placement process
    private void StartPlacement()
    {
        isPlacing = true;
        placementStatusText.text = "Tap to place the object.";
    }

    // Place the object in the AR environment
    private void PlaceObject(Touch touch)
    {
        // Perform a raycast to detect a surface
        List<ARRaycastHit> hits = new List<ARRaycastHit>();
        if (arRaycastManager.Raycast(touch.position, hits, TrackableType.PlaneWithinPolygon))
        {
            // Get the hit pose
            Pose hitPose = hits[0].pose;

            // If an object is already spawned, move it to the new position
            if (spawnedObject != null)
            {
                spawnedObject.transform.position = hitPose.position;
                spawnedObject.transform.rotation = hitPose.rotation;
            }
            else
            {
                // Instantiate the object at the hit position
                spawnedObject = Instantiate(objectToPlace, hitPose.position, hitPose.rotation);
                placementStatusText.text = "Object placed! Tap to move.";
            }
        }
    }

    // Method to remove the placed object
    public void RemoveObject()
    {
        if (spawnedObject != null)
        {
            Destroy(spawnedObject);
            spawnedObject = null;
            placementStatusText.text = "Object removed. Tap to place again.";
            isPlacing = false;
        }
    }
}
