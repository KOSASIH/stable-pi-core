from flask import Blueprint, request, jsonify
from web3 import Web3
from brownie import Stablecoin, Governance, accounts
import logging

api_routes = Blueprint('api', __name__)

# Initialize Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Adjust to your Ethereum node

# Load contracts dynamically
stablecoin_address = '0xYourStablecoinContractAddress'  # Replace with your contract address
governance_address = '0xYourGovernanceContractAddress'  # Replace with your contract address
stablecoin = Stablecoin.at(stablecoin_address)
governance = Governance.at(governance_address)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_routes.route('/mint', methods=['POST'])
def mint_tokens():
    data = request.json
    recipient = data.get('recipient')
    amount = data.get('amount')

    if not recipient or not amount:
        logger.error("Minting failed: Recipient and amount are required.")
        return jsonify({"error": "Recipient and amount are required."}), 400

    try:
        tx = stablecoin.mint(recipient, amount, {'from': accounts[0]})
        logger.info(f"Tokens minted successfully: {tx.txid}")
        return jsonify({"message": "Tokens minted successfully.", "transaction_hash": tx.txid}), 200
    except Exception as e:
        logger.error(f"Minting failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_routes.route('/burn', methods=['POST'])
def burn_tokens():
    data = request.json
    amount = data.get('amount')

    if not amount:
        logger.error("Burning failed: Amount is required.")
        return jsonify({"error": "Amount is required."}), 400

    try:
        tx = stablecoin.burn(amount, {'from': accounts[0]})
        logger.info(f"Tokens burned successfully: {tx.txid}")
        return jsonify({"message": "Tokens burned successfully.", "transaction_hash": tx.txid}), 200
    except Exception as e:
        logger.error(f"Burning failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_routes.route('/create_proposal', methods=['POST'])
def create_proposal():
    data = request.json
    description = data.get('description')

    if not description:
        logger.error("Proposal creation failed: Description is required.")
        return jsonify({"error": "Description is required."}), 400

    try:
        tx = governance.createProposal(description, {'from': accounts[0]})
        logger.info(f"Proposal created successfully: {tx.txid}")
        return jsonify({"message": "Proposal created successfully.", "transaction_hash": tx.txid}), 200
    except Exception as e:
        logger.error(f"Proposal creation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_routes.route('/vote', methods=['POST'])
def vote():
    data = request.json
    proposal_id = data.get('proposal_id')

    if not proposal_id:
        logger.error("Voting failed: Proposal ID is required.")
        return jsonify({"error": "Proposal ID is required."}), 400

    try:
        tx = governance.vote(proposal_id, {'from': accounts[1]})  # Assuming account[1] is the voter
        logger.info(f"Vote cast successfully: {tx.txid}")
        return jsonify({"message": "Vote cast successfully.", "transaction_hash": tx.txid}), 200
    except Exception as e:
        logger.error(f"Voting failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_routes.route('/execute_proposal', methods=['POST'])
def execute_proposal():
    data = request.json
    proposal_id = data.get('proposal_id')

    if not proposal_id:
        logger.error("Execution failed: Proposal ID is required.")
        return jsonify({"error": "Proposal ID is required."}),  400

    try:
        tx = governance.executeProposal(proposal_id, {'from': accounts[0]})
        logger.info(f"Proposal executed successfully: {tx.txid}")
        return jsonify({"message": "Proposal executed successfully.", "transaction_hash": tx.txid}), 200
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_routes.route('/get_balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')

    if not address:
        logger.error("Balance retrieval failed: Address is required.")
        return jsonify({"error": "Address is required."}), 400

    try:
        balance = stablecoin.balanceOf(address)
        logger.info(f"Balance retrieved successfully for {address}: {balance}")
        return jsonify({"address": address, "balance": balance}), 200
    except Exception as e:
        logger.error(f"Balance retrieval failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_routes.route('/get_proposal_status', methods=['GET'])
def get_proposal_status():
    proposal_id = request.args.get('proposal_id')

    if not proposal_id:
        logger.error("Proposal status retrieval failed: Proposal ID is required.")
        return jsonify({"error": "Proposal ID is required."}), 400

    try:
        status = governance.getProposalStatus(proposal_id)
        logger.info(f"Proposal status retrieved successfully for {proposal_id}: {status}")
        return jsonify({"proposal_id": proposal_id, "status": status}), 200
    except Exception as e:
        logger.error(f"Proposal status retrieval failed: {str(e)}")
        return jsonify({"error": str(e)}), 500
