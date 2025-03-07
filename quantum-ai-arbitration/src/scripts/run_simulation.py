# scripts/run_simulation.py

import logging
from quantum.quantum_solver import QuantumSolver

def main():
    """Main function to run the quantum simulation."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the quantum solver
    quantum_solver = QuantumSolver(backend='qasm_simulator', shots=1024)

    # Define a sample optimization problem
    problem = [100, 200, 300]

    # Run the optimization
    logging.info("Running quantum optimization...")
    result = quantum_solver.solve_optimization(problem)

    # Output the results
    logging.info("Optimization Result: %s", result)

if __name__ == "__main__":
    main()
