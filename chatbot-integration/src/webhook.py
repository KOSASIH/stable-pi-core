import os
import logging
from flask import Blueprint, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from utils.input_handler import sanitize_input
from utils.response_generator import generate_response
from intents.greeting_intent import handle_greeting_intent  # Import the greeting intent handler

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Flask Blueprint for the webhook
webhook_bp = Blueprint('webhook', __name__)

# Initialize Dialogflow client
DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = os.getenv('DIALOGFLOW_LANGUAGE_CODE', 'en')
DIALOGFLOW_SESSION_ID = os.getenv('DIALOGFLOW_SESSION_ID', '123456')

sessions_client = dialogflow.SessionsClient()

@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handles incoming messages from the bot framework or other sources."""
    try:
        req = request.get_json(silent=True, force=True)
        logger.info(f"Received request: {req}")

        # Extract user input
        user_input = sanitize_input(req.get('queryResult', {}).get('queryText', ''))
        session = sessions_client.session_path(DIALOGFLOW_PROJECT_ID, DIALOGFLOW_SESSION_ID)

        # Check for greeting intent
        if "greeting" in req.get('queryResult', {}).get('intent', {}).get('displayName', '').lower():
            bot_response = handle_greeting_intent(user_input)
            return jsonify({'fulfillmentText': bot_response})

        # Send user input to Dialogflow for other intents
        text_input = dialogflow.TextInput(text=user_input, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.QueryInput(text=text_input)

        response = sessions_client.detect_intent(session=session, query_input=query_input)
        logger.info(f"Dialogflow response: {response}")

        # Generate response based on Dialogflow's reply
        bot_response = generate_response(response)
        return jsonify({'fulfillmentText': bot_response})

    except InvalidArgument as e:
        logger.error(f"Invalid argument: {e}")
        return jsonify({'fulfillmentText': 'Sorry, I encountered an error processing your request.'}), 400
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'fulfillmentText': 'An unexpected error occurred. Please try again later.'}), 500
