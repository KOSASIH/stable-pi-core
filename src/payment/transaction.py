# payment/transaction.py

class Transaction:
    def __init__(self, user_id, amount, currency):
        self.transaction_id = str(uuid.uuid4())
        self.user_id = user_id
        self.amount = amount
        self.currency = currency
        self.status = 'pending'

    def __repr__(self):
        return f"<Transaction {self.transaction_id}: {self.amount} {self.currency} - {self.status}>"
