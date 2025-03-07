import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimulationTool:
    def __init__(self):
        self.simulation_data = {
            "stake": {
                "description": "You have staked your tokens.",
                "expected_return": lambda: random.uniform(0.03, 0.07),  # 3% to 7% return
            },
            "trade": {
                "description": "You have executed a trade.",
                "expected_return": lambda: random.uniform(-0.05, 0.10),  # -5% to 10% profit/loss
            },
            "hold": {
                "description": "You have decided to hold your tokens.",
                "expected_return": lambda: 0.0,  # No change
            }
        }

    def run_simulation(self, user_decision):
        """Simulate the impact of a user's decision on the ecosystem."""
        user_decision = user_decision.lower()

        if user_decision not in self.simulation_data:
            logging.warning(f"Invalid decision: {user_decision}")
            return "Decision not recognized. Please try 'stake', 'trade', or 'hold'."

        # Get simulation details
        simulation = self.simulation_data[user_decision]
        description = simulation["description"]
        expected_return = simulation["expected_return"]()

        # Log the simulation request
        logging.info(f"User  Decision: {user_decision} | Expected Return: {expected_return:.2f}")

        # Construct the result message
        result_message = f"{description} Expected return: {expected_return:.2f} (in percentage)."
        return result_message

# Example usage
if __name__ == "__main__":
    simulation_tool = SimulationTool()
    while True:
        user_decision = input("Enter your decision (stake, trade, hold) or 'exit' to quit: ")
        if user_decision.lower() == "exit":
            break
        result = simulation_tool.run_simulation(user_decision)
        print(result)
