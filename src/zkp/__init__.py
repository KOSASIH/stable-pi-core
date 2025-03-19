
# zkp/__init__.py

# Importing the necessary classes and functions from the ZKP module
from .zkp_prover import ZKProof
from .zkp_verifier import ZKVerifier
from .zkp_circuit import ZKCircuit
from .zkp_utils import (
    generate_random_secret,
    hash_value,
    generate_salt,
    create_commitment,
    encode_base64,
    decode_base64,
    generate_proof,
    verify_proof
)
from .zkp_generator import ZKPGenerator  # Importing the new ZKPGenerator class

__all__ = [
    "ZKProof",
    "ZKVerifier",
    "ZKCircuit",
    "ZKPGenerator",  # Adding ZKPGenerator to the public interface
    "generate_random_secret",
    "hash_value",
    "generate_salt",
    "create_commitment",
    "encode_base64",
    "decode_base64",
    "generate_proof",
    "verify_proof"
]
