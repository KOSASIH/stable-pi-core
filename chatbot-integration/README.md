# Chatbot Integration

## Overview

Chatbot Integration is a sophisticated chatbot application that leverages natural language processing (NLP) to provide users with an interactive experience. This project integrates with Dialogflow and the Microsoft Bot Framework, allowing for seamless communication and support. The chatbot can handle various intents, including greetings, frequently asked questions (FAQs), and customer support queries.

## Features

- **Natural Language Processing**: Utilizes NLTK and spaCy for understanding user inputs.
- **Dynamic Responses**: Generates personalized responses based on user context.
- **Webhook Support**: Handles real-time communication with users.
- **Testing Framework**: Includes unit tests for ensuring functionality and reliability.
- **Logging**: Advanced logging capabilities for tracking application behavior.
- **API Documentation**: Automatically generated API documentation using Flasgger.

## Technologies Used

- Python
- Flask
- NLTK
- spaCy
- Requests
- SQLAlchemy (optional)
- Dialogflow API (optional)
- Microsoft Bot Framework (optional)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/KOSASIH/stable-pi-core.git
cd stable-pi-core/chatbot-integration
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the root directory and add your environment variables. For example:

```plaintext
DIALOGFLOW_PROJECT_ID=your_project_id
DIALOGFLOW_CLIENT_EMAIL=your_client_email
DIALOGFLOW_PRIVATE_KEY=your_private_key
BOT_FRAMEWORK_APP_ID=your_app_id
BOT_FRAMEWORK_APP_PASSWORD=your_app_password
```

## Usage

### Running the Application

To start the Flask server, run the following command:

```bash
python src/main.py
```

The server will start on `http://127.0.0.1:5000/` by default.

### Webhook Configuration

Configure your webhook in Dialogflow or Microsoft Bot Framework to point to your Flask server's endpoint (e.g., `/webhook`).

### Testing

To run the unit tests, use the following command:

```bash
python -m unittest discover -s tests
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework used for building the application.
- [Dialogflow](https://dialogflow.cloud.google.com/) - The natural language understanding platform.
- [Microsoft Bot Framework](https://dev.botframework.com/) - The framework for building chatbots.
- [NLTK](https://www.nltk.org/) - The Natural Language Toolkit for Python.
- [spaCy](https://spacy.io/) - An NLP library for advanced processing.
