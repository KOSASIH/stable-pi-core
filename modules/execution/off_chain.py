import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OffChainExecution:
    def __init__(self, api_url: str):
        """Initialize the off-chain execution environment."""
        self.api_url = api_url
        logging.info(f"Off-chain execution initialized with API URL: {api_url}")

    def execute_task(self, task_data: dict) -> dict:
        """Execute a task off-chain and return the result."""
        logging.info(f"Executing off-chain task with data: {task_data}")
        response = requests.post(self.api_url, json=task_data)

        if response.status_code == 200:
            logging.info("Off-chain task executed successfully.")
            return response.json()
        else:
            logging.error(f"Off-chain task execution failed with status code: {response.status_code}")
            return {"error": "Execution failed", "status_code": response.status_code}

# Example usage
if __name__ == "__main__":
    off_chain_executor = OffChainExecution("https://api.example.com/execute")
    
    # Simulate an off-chain task execution
    task_data = {
        "task": "calculate",
        "value1": 10,
        "value2": 20
    }
    result = off_chain_executor.execute_task(task_data)
    print(f"Off-chain execution result: {result}")
