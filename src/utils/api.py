from flask import Flask, request, jsonify
from governance import GalacticGovernanceFramework

app = Flask(__name__)
governance = GalacticGovernanceFramework()

@app.route('/proposals', methods=['POST'])
def create_proposal():
    data = request.json
    proposal_id = data.get('proposal_id')
    description = data.get('description')
    proposer = data.get('proposer')
    expiration_time = data.get('expiration_time', 3600)  # Default to 1 hour

    success = governance.create_proposal(proposal_id, description, proposer, expiration_time)
    if success:
        return jsonify({"message": "Proposal created successfully."}), 201
    else:
        return jsonify({"error": "Proposal ID already exists."}), 400

@app.route('/proposals/<proposal_id>/vote', methods=['POST'])
def vote():
    data = request.json
    voter = data.get('voter')
    vote = data.get('vote')

    success = governance.vote(proposal_id, voter, vote)
    if success:
        return jsonify({"message": "Vote cast successfully."}), 200
    else:
        return jsonify({"error": "Failed to cast vote."}), 400

@app.route('/proposals/<proposal_id>/finalize', methods=['POST'])
def finalize_proposal():
    result = governance.finalize_proposal(proposal_id)
    if result:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": "Proposal does not exist."}), 404

@app.route('/proposals/<proposal_id>/status', methods=['GET'])
def get_proposal_status():
    status = governance.get_proposal_status(proposal_id)
    if status:
        return jsonify({"status": status}), 200
    else:
        return jsonify({"error": "Proposal does not exist."}), 404

@app.route('/proposals/<proposal_id>/votes', methods=['GET'])
def get_votes():
    decrypted_votes = governance.decrypt_votes(proposal_id)
    return jsonify({"votes": decrypted_votes}), 200

if __name__ == '__main__':
    app.run(debug=True)
