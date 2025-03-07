import json
from web3 import Web3

def load_contract(w3):
    # Load the contract information
    with open('dao_contract_info.json', 'r') as f:
        contract_info = json.load(f)

    # Create the contract instance
    dao_contract = w3.eth.contract(address=contract_info['address'], abi=contract_info['abi'])
    return dao_contract

def create_proposal(w3, dao_contract, admin_account):
    description = input("Enter proposal description: ")
    tx_hash = dao_contract.functions.createProposal(description).transact({'from': admin_account})
    w3.eth.waitForTransactionReceipt(tx_hash)
    print("Proposal created successfully.")

def vote(w3, dao_contract, voter_account):
    proposal_id = int(input("Enter proposal ID to vote on: "))
    tx_hash = dao_contract.functions.vote(proposal_id).transact({'from': voter_account})
    w3.eth.waitForTransactionReceipt(tx_hash)
    print("Vote recorded successfully.")

def execute_proposal(w3, dao_contract, admin_account):
    proposal_id = int(input("Enter proposal ID to execute: "))
    tx_hash = dao_contract.functions.executeProposal(proposal_id).transact({'from': admin_account})
    w3.eth.waitForTransactionReceipt(tx_hash)
    print("Proposal executed successfully.")

def main():
    # Connect to the Ethereum network (e.g., Ganache)
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Change to your provider
    assert w3.isConnected(), "Failed to connect to the Ethereum network"

    # Load the DAO contract
    dao_contract = load_contract(w3)

    # Set the admin account (the account that deployed the contract)
    admin_account = w3.eth.accounts[0]  # Change as needed
    print(f"Using admin account: {admin_account}")

    while True:
        print("\nOptions:")
        print("1. Create Proposal")
        print("2. Vote on Proposal")
        print("3. Execute Proposal")
        print("4. Exit")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            create_proposal(w3, dao_contract, admin_account)
        elif choice == '2':
            voter_account = input("Enter your account address: ")
            vote(w3, dao_contract, voter_account)
        elif choice == '3':
            execute_proposal(w3, dao_contract, admin_account)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
