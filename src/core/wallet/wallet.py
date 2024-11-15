import json
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from datetime import datetime

class Wallet:
    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.private_key.public_key()
        self.balances = {
            "USD": 1000.0,
            "ETH": 5.0,
            "BTC": 0.1,
        }
        self.transaction_history = []

    def generate_private_key(self):
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

    def export_private_key(self, password=None):
        encryption_algorithm = serialization.BestAvailableEncryption(password) if password else serialization.NoEncryption()
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=encryption_algorithm
        )

    def export_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def get_balance(self, currency):
        return self.balances.get(currency, 0)

    def transfer(self, to_wallet, currency, amount):
        if currency not in self.balances:
            raise ValueError("Currency not supported.")
        if self.balances[currency] < amount:
            raise ValueError("Insufficient balance.")

        self.balances[currency] -= amount
        to_wallet.balances[currency] += amount
        self.record_transaction(to_wallet, currency, amount)

    def record_transaction(self, to_wallet, currency, amount):
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "to": to_wallet.export_public_key().decode(),
            "currency": currency,
            "amount": amount
        }
        self.transaction_history.append(transaction)

    def get_transaction_history(self):
        return self.transaction_history

if __name__ == "__main__":
    wallet1 = Wallet()
    wallet2 = Wallet()

    print("Wallet 1 Balance (ETH):", wallet1.get_balance("ETH"))
    print("Wallet 2 Balance (ETH):", wallet2.get_balance("ETH"))

    wallet1.transfer(wallet2, "ETH", 1.0)

    print("Wallet 1 Balance (ETH) after transfer:", wallet1.get_balance("ETH"))
    print("Wallet 2 Balance (ETH) after transfer:", wallet2.get_balance("ETH"))
    print("Transaction History:", wallet1.get_transaction_history())
