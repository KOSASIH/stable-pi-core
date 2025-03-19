import asyncio
from aiocoap import *
import yaml
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config/coap-config.yaml', 'r') as file:
    coap_config = yaml.safe_load(file)

# CoAP settings
coap_server = coap_config['coap']['server']
resource_path = coap_config['coap']['resource_path']

async def coap_request(method='GET', payload=None):
    """
    Send a CoAP request to the specified server and handle the response.
    
    Parameters:
        method (str): The HTTP method to use ('GET' or 'POST').
        payload (dict): The payload to send with the request (for POST).
    """
    # Create a CoAP context
    protocol = await Context.create_client_context()

    # Construct the request
    uri = f"{coap_server}/{resource_path}"
    request = Message(code=GET if method == 'GET' else POST, uri=uri)

    if method == 'POST' and payload is not None:
        request.payload = json.dumps(payload).encode('utf-8')
        request.opt.content_format = 50  # Application/JSON

    try:
        # Send the request and wait for the response
        response = await protocol.request(request).response
        logging.info(f"Response from CoAP server: {response.payload.decode()}")
    except Exception as e:
        logging.error(f"Failed to send CoAP request: {e}")

if __name__ == "__main__":
    # Example usage
    try:
        # Send a GET request
        asyncio.run(coap_request(method='GET'))

        # Send a POST request with sample data
        sample_payload = {
            'temperature': 25.0,
            'humidity': 60.0
        }
        asyncio.run(coap_request(method='POST', payload=sample_payload))

    except KeyboardInterrupt:
        logging.info("CoAP client stopped by user.")
