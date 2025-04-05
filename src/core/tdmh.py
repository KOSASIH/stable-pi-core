import time
import json

class TransDimensionalMarketHub:
    def __init__(self):
        self.market_data = {}
        self.transaction_log = []

    def list_item(self, item_id, item_name, price, description, quantity):
        """List a new item in the market with details."""
        self.market_data[item_id] = {
            'name': item_name,
            'price': price,
            'description': description,
            'quantity': quantity
        }
        print(f"Item '{item_name}' listed for {price} with ID {item_id} in TDMH.")

    def trade_item(self, item_id, buyer, quantity):
        """Trade an item for a buyer, checking stock and logging the transaction."""
        if item_id not in self.market_data:
            print("Item not available.")
            return

        item = self.market_data[item_id]
        if item['quantity'] < quantity:
            print(f"Insufficient stock for item '{item['name']}'. Available: {item['quantity']}, Requested: {quantity}.")
            return

        total_price = item['price'] * quantity
        self.log_transaction(item['name'], buyer, quantity, total_price)
        item['quantity'] -= quantity  # Reduce stock
        print(f"{buyer} purchased {quantity} of '{item['name']}' for {total_price}. Remaining stock: {item['quantity']}.")

    def log_transaction(self, item_name, buyer, quantity, total_price):
        """Log the transaction details."""
        transaction = {
            'item_name': item_name,
            'buyer': buyer,
            'quantity': quantity,
            'total_price': total_price,
            'timestamp': time.time()
        }
        self.transaction_log.append(transaction)
        print(f"Transaction logged: {json.dumps(transaction)}")

    def get_transaction_log(self):
        """Retrieve the transaction log."""
        return self.transaction_log

    def update_price(self, item_id, new_price):
        """Update the price of an item."""
        if item_id in self.market_data:
            self.market_data[item_id]['price'] = new_price
            print(f"Price for item '{self.market_data[item_id]['name']}' updated to {new_price}.")
        else:
            print("Item not found.")

    def check_item_details(self, item_id):
        """Check details of an item."""
        if item_id in self.market_data:
            return self.market_data[item_id]
        else:
            print("Item not found.")
            return None

# Example usage
if __name__ == "__main__":
    tdmh = TransDimensionalMarketHub()
    tdmh.list_item("item_001", "Galactic Crystal", 100, "A rare crystal from the Andromeda galaxy.", 50)
    tdmh.list_item("item_002", "Quantum Energy Cell", 250, "A cell that powers intergalactic devices.", 30)

    tdmh.trade_item("item_001", "User _1", 5)
    print("Transaction Log:", tdmh.get_transaction_log())

    tdmh.update_price("item_001", 120)
    tdmh.trade_item("item_001", "User _2", 10)
    print("Transaction Log:", tdmh.get_transaction_log())

    item_details = tdmh.check_item_details("item_001")
    print("Item Details:", item_details)
