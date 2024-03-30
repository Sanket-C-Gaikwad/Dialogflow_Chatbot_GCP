from flask import Flask, request, jsonify, render_template
from google.cloud import dialogflow
from google.oauth2 import service_account
from uuid import uuid4
import os

app = Flask(__name__)

def create_unique_session_id():
    # Generates a unique session ID
    return str(uuid4())

def get_credentials():
    # Load the service account credentials once and create an authenticated session
    file_path = 'service-account-file.json'
    return service_account.Credentials.from_service_account_file(file_path)

credentials = get_credentials()  # Get credentials once and reuse

def send_to_dialogflow(message, project_id, session_id, credentials):
    language_code = "en"
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=message, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    return {"fulfillmentText": response.query_result.fulfillment_text}

@app.route('/send_message', methods=['POST'])
def send_message():
    session_id = create_unique_session_id()  # Create a unique session ID for each conversation
    message = request.json['message']  # Updated to handle JSON payload
    project_id = 'image-classification-402513'  # Replace with your Dialogflow project ID

    response = send_to_dialogflow(message, project_id, session_id, credentials)
    return jsonify(response)

@app.route('/')
def home():
    # Serve the HTML interface for interacting with the chatbot
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)  # Consider using debug=False in production
