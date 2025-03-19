using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class VRController : MonoBehaviour
{
    [Header("XR Components")]
    [SerializeField] private XRController controller; // Reference to the XR Controller
    [SerializeField] private GameObject objectToInteract; // The object to interact with
    [SerializeField] private float interactionDistance = 2.0f; // Maximum interaction distance

    private XRGrabInteractable grabInteractable; // Reference to the interactable component

    void Start()
    {
        // Get the XRGrabInteractable component from the object to interact with
        if (objectToInteract != null)
        {
            grabInteractable = objectToInteract.GetComponent<XRGrabInteractable>();
        }
    }

    void Update()
    {
        // Check for input to interact with the object
        if (controller.selectInteractionState.activatedThisFrame)
        {
            TryInteract();
        }
    }

    // Attempt to interact with the object
    private void TryInteract()
    {
        // Perform a raycast to check if the object is within interaction distance
        RaycastHit hit;
        if (Physics.Raycast(controller.transform.position, controller.transform.forward, out hit, interactionDistance))
        {
            if (hit.collider.gameObject == objectToInteract)
            {
                // If the object is interactable, grab it
                if (grabInteractable != null)
                {
                    grabInteractable.OnSelectEntered(new SelectEnterEventArgs());
                }
            }
        }
    }

    // Method to release the object
    public void ReleaseObject()
    {
        if (grabInteractable != null)
        {
            grabInteractable.OnSelectExited(new SelectExitEventArgs());
        }
    }
}
