import hashlib
import os
import random
import base64

def generate_random_secret(min_value=1, max_value=100):
    """Generate a random secret value within a specified range."""
    return random.randint(min_value, max_value)

def hash_value(value):
    """Hash a given value using SHA-256."""
    return hashlib.sha256(value.encode()).hexdigest()

def generate_salt(length=16):
    """Generate a random salt of specified length."""
    return os.urandom(length)

def create_commitment(secret, salt):
    """Create a commitment to the secret using a salt."""
    return hash_value(salt.hex() + str(secret))

def encode_base64(data):
    """Encode data to Base64."""
    return base64.b64encode(data).decode()

def decode_base64(encoded_data):
    """Decode Base64 encoded data."""
    return base64.b64decode(encoded_data)

def generate_proof(guess):
    """Generate a proof for the guess."""
    return hash_value(str(guess))

def verify_proof(guess, proof):
    """Verify the proof against the guess."""
    expected_proof = generate_proof(guess)
    return expected_proof == proof

# Example usage
if __name__ == "__main__":
    # Generate a random secret
    secret = generate_random_secret()
    print(f"Generated Secret: {secret}")

    # Generate a salt
    salt = generate_salt()
    print(f"Generated Salt: {salt.hex()}")

    # Create a commitment
    commitment = create_commitment(secret, salt)
    print(f"Commitment: {commitment}")

    # Generate proof for a guess
    guess = int(input("Enter your guess for the secret: "))
    proof = generate_proof(guess)
    print(f"Generated Proof: {proof}")

    # Verify the proof
    if verify_proof(guess, proof):
        print("Verification successful: The guess is correct!")
    else:
        print("Verification failed: The guess is incorrect.")
