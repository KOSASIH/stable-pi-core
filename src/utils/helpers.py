from web3 import Web3

def is_valid_address(address):
    """Check if the provided address is a valid Ethereum address with checksum validation."""
    if not Web3.isAddress(address):
        return False
    return Web3.toChecksumAddress(address) == address

def to_wei(amount, unit='ether'):
    """Convert an amount to Wei."""
    try:
        return Web3.toWei(amount, unit)
    except Exception as e:
        raise ValueError(f"Error converting to Wei: {e}")

def from_wei(amount, unit='ether'):
    """Convert an amount from Wei to a specified unit."""
    try:
        return Web3.fromWei(amount, unit)
    except Exception as e:
        raise ValueError(f"Error converting from Wei: {e}")

def estimate_gas_price(web3):
    """Estimate the current gas price on the Ethereum network."""
    try:
        gas_price = web3.eth.gas_price
        return gas_price
    except Exception as e:
        raise RuntimeError(f"Error estimating gas price: {e}")

def create_transaction(to_address, value, gas=21000, gas_price=None, nonce=None):
    """Create a transaction object."""
    if not is_valid_address(to_address):
        raise ValueError("Invalid recipient address.")
    
    transaction = {
        'to': to_address,
        'value': to_wei(value, 'ether'),  # Convert value to Wei
        'gas': gas,
        'nonce': nonce,
    }
    
    if gas_price is not None:
        transaction['gasPrice'] = gas_price
    else:
        transaction['gasPrice'] = estimate_gas_price(Web3)  # Use estimated gas price if not provided

    return transaction

# Example usage
if __name__ == "__main__":
    # Initialize Web3 instance (replace with your Ethereum node URL)
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

    print(is_valid_address('0x32Be343B94f860124dC4fEe278FDCBD38C102D88'))  # True
    print(to_wei(1, 'ether'))  # 1000000000000000000
    print(from_wei(1000000000000000000, 'ether'))  # 1.0

    # Estimate gas price
    print(f"Estimated Gas Price: {from_wei(estimate_gas_price(web3), 'gwei')} Gwei")

    # Create a transaction
    transaction = create_transaction('0x32Be343B94f860124dC4fEe278FDCBD38C102D88', 0.1)
    print("Transaction:", transaction)
