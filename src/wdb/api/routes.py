# src/wdb/api/routes.py

from fastapi import APIRouter, HTTPException
from wdb import DataTransferProtocol, NodeNetwork, PredictiveAlgorithm, QuantumEntanglement

router = APIRouter()

# Initialize components
data_transfer = DataTransferProtocol()
node_network = NodeNetwork()
predictive_algorithm = PredictiveAlgorithm()
quantum_entanglement = QuantumEntanglement()

@router.post("/transfer/")
async def transfer_data(source: str, destination: str, data: str):
    """
    Endpoint to initiate data transfer between nodes.
    """
    result = await data_transfer.initiate_transfer(source, destination, data)
    if result == "Transfer successful.":
        return {"message": result}
    else:
        raise HTTPException(status_code=400, detail="Transfer failed.")

@router.post("/nodes/")
async def add_node(node_id: str, location: str):
    """
    Endpoint to add a new node to the network.
    """
    try:
        node_network.add_node(node_id, location)
        return {"message": f"Node {node_id} added at {location}."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nodes/{node_id}")
async def get_node(node_id: str):
    """
    Endpoint to retrieve the location of a specific node.
    """
    location = node_network.get_node_location(node_id)
    if location == "Node not found.":
        raise HTTPException(status_code=404, detail=location)
    return {"node_id": node_id, "location": location}

@router.post("/predict/")
async def predict_data(future_time: list):
    """
    Endpoint to predict future data needs.
    """
    predictions = predictive_algorithm.predict(future_time)
    return {"predictions": predictions.tolist()}

@router.post("/entangle/")
async def entangle_data(data: str):
    """
    Endpoint to entangle data.
    """
result = await quantum_entanglement.entangle(data)
    return {"message": result}
