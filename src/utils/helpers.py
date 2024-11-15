from web3 import Web3

def is_valid_address(address):
    """Check if the provided address is a valid Ethereum address."""
    return Web3.isAddress(address)

def to_wei(amount, unit='ether'):
    """Convert an amount to Wei."""
    return Web3.toWei(amount, unit)

def from_wei(amount, unit='ether'):
    """Convert an amount from Wei to a specified unit."""
    return Web3.fromWei(amount, unit)

# Example usage
if __name__ == "__main__":
    print(is_valid_address('0x32Be343B94f860124dC4fEe278FDCBD38C102D88'))  # True
    print(to_wei(1, 'ether'))  # 1000000000000000000
    print(from_wei(1000000000000000000, 'ether'))  # 1.0
