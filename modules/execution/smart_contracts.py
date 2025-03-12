import json
import logging
from typing import Any, Dict, Callable, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmartContract:
    def __init__(self, contract_code: str):
        """Initialize the smart contract with its code."""
        self.contract_code = contract_code
        self.state = {}  # Store the state of the contract
        self.event_listeners = []  # List of event listeners

    def execute(self, function_name: str, *args: Any) -> Any:
        """Execute a function in the smart contract."""
        logging.info(f"Executing {function_name} with arguments: {args}")
        if function_name not in self.contract_functions():
            logging.error(f"Function {function_name} not found in contract.")
            return None

        # Call the function dynamically
        function = self.contract_functions()[function_name]
        result = function(*args)

        # Emit an event after execution
        self.emit_event(function_name, args)
        return result

    def contract_functions(self) -> Dict[str, Callable]:
        """Define the functions available in the smart contract."""
        return {
            "set_value": self.set_value,
            "get_value": self.get_value,
        }

    def set_value(self, key: str, value: Any):
        """Set a value in the contract state."""
        self.state[key] = value
        logging.info(f"Set value: {key} = {value}")

    def get_value(self, key: str) -> Any:
        """Get a value from the contract state."""
        value = self.state.get(key, None)
        logging.info(f"Get value: {key} = {value}")
        return value

    def emit_event(self, event_name: str, args: List[Any]):
        """Emit an event to all registered listeners."""
        logging.info(f"Emitting event: {event_name} with arguments: {args}")
        for listener in self.event_listeners:
            listener(event_name, args)

    def add_event_listener(self, listener: Callable[[str, List[Any]], None]):
        """Add an event listener."""
        self.event_listeners.append(listener)
        logging.info(f"Added event listener: {listener}")

    def save_state(self, filename: str):
        """Save the contract state to a file."""
        with open(filename, 'w') as file:
            json.dump(self.state, file)
            logging.info(f"Contract state saved to {filename}")

    def load_state(self, filename: str):
        """Load the contract state from a file."""
        try:
            with open(filename, 'r') as file:
                self.state = json.load(file)
                logging.info(f"Contract state loaded from {filename}")
        except FileNotFoundError:
            logging.warning(f"State file {filename} not found. Starting with an empty state.")
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from {filename}. State not loaded.")

# Example usage
if __name__ == "__main__":
    contract_code = "Sample Smart Contract Code"
    contract = SmartContract(contract_code)

    # Add an event listener
    def event_listener(event_name: str, args: List[Any]):
        print(f"Event: {event_name}, Args: {args}")

    contract.add_event_listener(event_listener)

    # Execute smart contract functions
    contract.execute("set_value", "name", "Alice")
    name = contract.execute("get_value", "name")
    print(f"Retrieved Name: {name}")

    # Save and load state
    contract.save_state("contract_state.json")
    contract.load_state("contract_state.json")
