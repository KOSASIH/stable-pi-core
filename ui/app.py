from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from ai_assistant import AIAssistant
from simulation_tool import SimulationTool
from dao import DAO  # Assuming you have a DAO class for interacting with the DAO contract
import logging
import os

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_default_secret_key')  # Use environment variable
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize AI Assistant, Simulation Tool, and DAO
ai_assistant = AIAssistant()
simulation_tool = SimulationTool()
dao = DAO()  # Initialize your DAO class

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the user."""
    try:
        user_input = request.json.get('message')
        response = ai_assistant.get_response(user_input)
        logging.info(f":User  {user_input} | AI: {response}")
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@app.route('/simulate', methods=['POST'])
def simulate():
    """Run a simulation based on user input."""
    try:
        user_decision = request.json.get('decision')
        result = simulation_tool.run_simulation(user_decision)
        logging.info(f"User  Decision: {user_decision} | Simulation Result: {result}")
        return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error in simulate endpoint: {e}")
        return jsonify({'error': 'An error occurred while running the simulation.'}), 500

@app.route('/session', methods=['GET', 'POST'])
def manage_session():
    """Manage user session data."""
    if request.method == 'POST':
        session['user_data'] = request.json
        logging.info(f"Session data updated: {session['user_data']}")
        return jsonify({'status': 'Session data updated.'})
    return jsonify({'user_data': session.get('user_data', {})})

@app.route('/dao/proposals', methods=['POST'])
def create_proposal():
    """Create a new proposal in the DAO."""
    try:
        proposal_description = request.json.get('description')
        proposal_id = dao.create_proposal(proposal_description)  # Assuming create_proposal returns the proposal ID
        logging.info(f"Proposal created: {proposal_id} | Description: {proposal_description}")
        return jsonify({'status': 'Proposal created', 'proposal_id': proposal_id}), 201
    except Exception as e:
        logging.error(f"Error creating proposal: {e}")
        return jsonify({'error': 'An error occurred while creating the proposal.'}), 500

@app.route('/dao/vote', methods=['POST'])
def vote():
    """Vote on a proposal in the DAO."""
    try:
        proposal_id = request.json.get('proposal_id')
        dao.vote(proposal_id)  # Assuming vote method handles the voting logic
        logging.info(f"User  voted on proposal: {proposal_id}")
        return jsonify({'status': 'Vote recorded'}), 200
    except Exception as e:
        logging.error(f"Error voting on proposal: {e}")
        return jsonify({'error': 'An error occurred while voting.'}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Error starting the application: {e}")
