import hashlib
import os
import random

class ZKProof:
    def __init__(self):
        self.secret = None
        self.commitment = None

    def generate_secret(self):
        """Generate a random secret value."""
        self.secret = random.randint(1, 100)  # Secret value between 1 and 100
        self.commitment = self.commit(self.secret)

    def commit(self, secret):
        """Create a commitment to the secret."""
        # Using a simple hash function for commitment
        salt = os.urandom(16)  # Generate a random salt
        return hashlib.sha256(salt + str(secret).encode()).hexdigest()

    def generate_proof(self, guess):
        """Generate a proof that the guess is equal to the secret."""
        if self.secret is None:
            raise ValueError("Secret not generated. Call generate_secret() first.")
        
        # The proof is simply the hash of the guess
        proof = hashlib.sha256(str(guess).encode()).hexdigest()
        return proof

    def verify(self, guess, proof):
        """Verify the proof against the commitment."""
        # Recreate the hash of the guess and compare it to the proof
        expected_proof = hashlib.sha256(str(guess).encode()).hexdigest()
        return expected_proof == proof

# Example usage
if __name__ == "__main__":
    zkp = ZKProof()
    zkp.generate_secret()  # Generate a secret

    # Prover guesses the secret
    guess = int(input("Enter your guess for the secret (1-100): "))
    proof = zkp.generate_proof(guess)  # Generate proof for the guess

    # Verifier checks the proof
    if zkp.verify(guess, proof):
        print("Verified: The guess is correct!")
    else:
        print("Verification failed: The guess is incorrect.")
