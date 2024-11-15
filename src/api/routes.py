from flask import Blueprint, request, jsonify
from web3 import Web3
from brownie import Stablecoin, Governance, accounts

api_routes = Blueprint('api', __name__)

# Initialize Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Adjust to your Ethereum node

# Load contracts
stablecoin = Stablecoin.at('0xYourStablecoinContractAddress')
governance = Governance.at('0xYourGovernanceContractAddress')

@api_routes.route('/mint', methods=['POST'])
def mint_tokens():
    data = request.json
    recipient = data.get('recipient')
    amount = data.get('amount')

    if not recipient or not amount:
        return jsonify({"error": "Recipient and amount are required."}), 400

    stablecoin.mint(recipient, amount, {'from': accounts[0]})
    return jsonify({"message": "Tokens minted successfully."}), 200

@api_routes.route('/burn', methods=['POST'])
def burn_tokens():
    data = request.json
    amount = data.get('amount')

    if not amount:
        return jsonify({"error": "Amount is required."}), 400

    stablecoin.burn(amount, {'from': accounts[0]})
    return jsonify({"message": "Tokens burned successfully."}), 200

@api_routes.route('/create_proposal', methods=['POST'])
def create_proposal():
    data = request.json
    description = data.get('description')

    if not description:
        return jsonify({"error": "Description is required."}), 400

    governance.createProposal(description, {'from': accounts[0]})
    return jsonify({"message": "Proposal created successfully."}), 200

@api_routes.route('/vote', methods=['POST'])
def vote():
    data = request.json
    proposal_id = data.get('proposal_id')

    if not proposal_id:
        return jsonify({"error": "Proposal ID is required."}), 400

    governance.vote(proposal_id, {'from': accounts[1]})  # Assuming account[1] is the voter
    return jsonify({"message": "Vote cast successfully."}), 200

@api_routes.route('/execute_proposal', methods=['POST'])
def execute_proposal():
    data = request.json
    proposal_id = data.get('proposal_id')

    if not proposal_id:
        return jsonify({"error": "Proposal ID is required."}), 400

    governance.executeProposal(proposal_id, {'from': accounts[0]})
    return jsonify({"message": "Proposal executed successfully."}), 200
