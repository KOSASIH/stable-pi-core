from flask import Flask, request, jsonify
from governance import GalacticGovernanceFramework
import logging

app = Flask(__name__)
governance = GalacticGovernanceFramework()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/proposals', methods=['POST'])
def create_proposal():
    data = request.json
    proposal_id = data.get('proposal_id')
    description = data.get('description')
    proposer = data.get('proposer')
    expiration_time = data.get('expiration_time', 3600)  # Default to 1 hour

    # Input validation
    if not proposal_id or not description or not proposer:
        return jsonify({"error": "Proposal ID, description, and proposer are required."}), 400

    try:
        success = governance.create_proposal(proposal_id, description, proposer, expiration_time)
        if success:
            logging.info(f"Proposal created: {proposal_id}")
            return jsonify({"message": "Proposal created successfully."}), 201
        else:
            return jsonify({"error": "Proposal ID already exists."}), 400
    except Exception as e:
        logging.error(f"Error creating proposal: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/proposals/<proposal_id>/vote', methods=['POST'])
def vote(proposal_id):
    data = request.json
    voter = data.get('voter')
    vote = data.get('vote')

    # Input validation
    if not voter or vote not in ['for', 'against']:
        return jsonify({"error": "Voter and valid vote choice ('for' or 'against') are required."}), 400

    try:
        success = governance.vote(proposal_id, voter, vote)
        if success:
            logging.info(f"Vote cast by {voter} on proposal {proposal_id}.")
            return jsonify({"message": "Vote cast successfully."}), 200
        else:
            return jsonify({"error": "Failed to cast vote."}), 400
    except Exception as e:
        logging.error(f"Error voting on proposal {proposal_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/proposals/<proposal_id>/finalize', methods=['POST'])
def finalize_proposal(proposal_id):
    try:
        result = governance.finalize_proposal(proposal_id)
        if result:
            logging.info(f"Proposal finalized: {proposal_id}")
            return jsonify({"result": result}), 200
        else:
            return jsonify({"error": "Proposal does not exist."}), 404
    except Exception as e:
        logging.error(f"Error finalizing proposal {proposal_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/proposals/<proposal_id>/status', methods=['GET'])
def get_proposal_status(proposal_id):
    try:
        status = governance.get_proposal_status(proposal_id)
        if status:
            return jsonify({"status": status}), 200
        else:
            return jsonify({"error": "Proposal does not exist."}), 404
    except Exception as e:
        logging.error(f"Error retrieving status for proposal {proposal_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/proposals/<proposal_id>/votes', methods=['GET'])
def get_votes(proposal_id):
    try:
        decrypted_votes = governance.decrypt_votes(proposal_id)
        return jsonify({"votes": decrypted_votes}), 200
    except Exception as e:
        logging.error(f"Error retrieving votes for proposal {proposal_id}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
