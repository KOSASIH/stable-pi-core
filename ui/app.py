from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from ai_assistant import AIAssistant
from simulation_tool import SimulationTool
import logging

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize AI Assistant and Simulation Tool
ai_assistant = AIAssistant()
simulation_tool = SimulationTool()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the user."""
    user_input = request.json.get('message')
    response = ai_assistant.get_response(user_input)
    logging.info(f":User  {user_input} | AI: {response}")
    return jsonify({'response': response})

@app.route('/simulate', methods=['POST'])
def simulate():
    """Run a simulation based on user input."""
    user_decision = request.json.get('decision')
    result = simulation_tool.run_simulation(user_decision)
    logging.info(f"User  Decision: {user_decision} | Simulation Result: {result}")
    return jsonify({'result': result})

@app.route('/session', methods=['GET', 'POST'])
def manage_session():
    """Manage user session data."""
    if request.method == 'POST':
        session['user_data'] = request.json
        logging.info(f"Session data updated: {session['user_data']}")
        return jsonify({'status': 'Session data updated.'})
    return jsonify({'user_data': session.get('user_data', {})})

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Error starting the application: {e}")
