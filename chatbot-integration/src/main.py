import os
import logging
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from utils.input_handler import sanitize_input
from utils.response_generator import generate_response

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize Dialogflow client
DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = os.getenv('DIALOGFLOW_LANGUAGE_CODE', 'en')
DIALOGFLOW_SESSION_ID = os.getenv('DIALOGFLOW_SESSION_ID', '123456')

sessions_client = dialogflow.SessionsClient()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handles incoming messages from the bot framework or other sources."""
    try:
        req = request.get_json(silent=True, force=True)
        logger.info(f"Received request: {json.dumps(req, indent=2)}")

        # Extract user input
        user_input = sanitize_input(req.get('queryResult', {}).get('queryText', ''))
        session = sessions_client.session_path(DIALOGFLOW_PROJECT_ID, DIALOGFLOW_SESSION_ID)

        # Send user input to Dialogflow
        text_input = dialogflow.TextInput(text=user_input, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.QueryInput(text=text_input)

        response = sessions_client.detect_intent(session=session, query_input=query_input)
        logger.info(f"Dialogflow response: {json.dumps(response, indent=2)}")

        # Generate response based on Dialogflow's reply
        bot_response = generate_response(response)
        return jsonify({'fulfillmentText': bot_response})

    except InvalidArgument as e:
        logger.error(f"Invalid argument: {e}")
        return jsonify({'fulfillmentText': 'Sorry, I encountered an error processing your request.'}), 400
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'fulfillmentText': 'An unexpected error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    # Start the Flask server
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
