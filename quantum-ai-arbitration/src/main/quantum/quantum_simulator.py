# src/main/quantum/quantum_simulator.py

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import logging

class QuantumSimulator:
    def __init__(self, backend='qasm_simulator', shots=1024):
        self.backend = backend
        self.shots = shots
        self.aer_simulator = Aer.get_backend(self.backend)
        logging.info("QuantumSimulator initialized with backend: %s and shots: %d", self.backend, self.shots)

    def create_circuit(self, num_qubits):
        """
        Create a quantum circuit with the specified number of qubits.
        
        Args:
            num_qubits (int): The number of qubits in the circuit.

        Returns:
            QuantumCircuit: The created quantum circuit.
        """
        qc = QuantumCircuit(num_qubits)
        logging.info("Created quantum circuit with %d qubits.", num_qubits)
        return qc

    def apply_hadamard(self, qc):
        """
        Apply Hadamard gates to all qubits in the circuit to create superposition.
        
        Args:
            qc (QuantumCircuit): The quantum circuit to modify.
        """
        qc.h(range(qc.num_qubits))
        logging.info("Applied Hadamard gates to create superposition.")

    def apply_cnot(self, qc, control, target):
        """
        Apply a CNOT gate to the circuit.
        
        Args:
            qc (QuantumCircuit): The quantum circuit to modify.
            control (int): The control qubit index.
            target (int): The target qubit index.
        """
        qc.cx(control, target)
        logging.info("Applied CNOT gate with control qubit %d and target qubit %d.", control, target)

    def measure(self, qc):
        """
        Measure all qubits in the circuit.
        
        Args:
            qc (QuantumCircuit): The quantum circuit to modify.
        """
        qc.measure_all()
        logging.info("Added measurement to all qubits.")

    def run_simulation(self, qc):
        """
        Run the quantum circuit simulation.
        
        Args:
            qc (QuantumCircuit): The quantum circuit to execute.

        Returns:
            dict: The counts of measurement results.
        """
        logging.info("Executing quantum circuit...")
        job = execute(qc, backend=self.aer_simulator, shots=self.shots)
        result = job.result()
        counts = result.get_counts(qc)
        logging.info("Simulation complete. Counts: %s", counts)
        return counts

    def visualize_results(self, counts):
        """
        Visualize the results of the quantum circuit execution.
        
        Args:
            counts (dict): The counts of measurement results.
        """
        plot_histogram(counts).show()
        logging.info("Results visualized.")

    def simulate(self, num_qubits):
        """
        Simulate a quantum circuit with the specified number of qubits.
        
        Args:
            num_qubits (int): The number of qubits to simulate.
        """
        qc = self.create_circuit(num_qubits)
        self.apply_hadamard(qc)

        # Example: Apply CNOT gates between qubits
        if num_qubits > 1:
            for i in range(num_qubits - 1):
                self.apply_cnot(qc, i, i + 1)

        self.measure(qc)
        counts = self.run_simulation(qc)
        self.visualize_results(counts)
