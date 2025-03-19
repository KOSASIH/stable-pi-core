# zkp/zkp_generator.py

import os
import hashlib
from zokrates_py import Zokrates

class ZKPGenerator:
    def __init__(self):
        self.zokrates = Zokrates()

    def generate_proof(self, secret):
        # Step 1: Create a circuit that proves knowledge of the secret
        circuit_code = f"""
        def main(private field secret) {{
            field result = secret * secret; // Example computation
            return result;
        }}
        """
        
        # Step 2: Compile the circuit
        self.zokrates.compile(circuit_code)

        # Step 3: Setup the trusted setup
        proving_key, verification_key = self.zokrates.setup()

        # Step 4: Generate the proof
        proof = self.zokrates.prove(proving_key, [secret])

        return proof, verification_key

    def verify_proof(self, proof, verification_key):
        # Step 5: Verify the proof
        is_valid = self.zokrates.verify(verification_key, proof)
        return is_valid

# Example usage
if __name__ == "__main__":
    zkp_gen = ZKPGenerator()
    
    # Prover's secret
    secret = 42  # This is the secret the prover knows

    # Generate proof
    proof, verification_key = zkp_gen.generate_proof(secret)
    print("Generated Proof:", proof)

    # Verify proof
    is_valid = zkp_gen.verify_proof(proof, verification_key)
    print("Is the proof valid?", is_valid)
