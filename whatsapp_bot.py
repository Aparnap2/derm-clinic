from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from agent.agent import get_patient_agent

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the agent
agent = get_patient_agent()

# WhatsApp API configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_ID = '652573494605608'  # Hardcoded since it's in the URL
WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'default_token')  # Get from environment variables

@app.route('/', methods=['GET'])
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Verify webhook URL with Facebook/Meta
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    print(f"Verification attempt - Mode: {mode}, Token: {token}")  # Debug log
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('WEBHOOK_VERIFIED')
            return challenge, 200
    return 'Verification failed', 403

@app.route('/', methods=['POST'])
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle incoming WhatsApp messages
    """
    try:
        data = request.get_json()
        
        if data['object'] == 'whatsapp_business_account':
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    value = change.get('value')
                    if value and 'messages' in value:
                        for message in value['messages']:
                            if message['type'] == 'text':
                                handle_message(
                                    phone_number=message['from'],
                                    message=message['text']['body']
                                )
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def handle_message(phone_number, message):
    """
    Process incoming message and send response
    """
    try:
        # Get response from agent
        response = agent(message)
        
        # Send response back via WhatsApp
        send_whatsapp_message(phone_number, response)
    except Exception as e:
        print(f"Error handling message: {str(e)}")
        send_whatsapp_message(phone_number, "Sorry, I encountered an error processing your request.")

def send_whatsapp_message(phone_number, message):
    """
    Send message via WhatsApp Business API
    """
    url = WHATSAPP_API_URL  # Use the URL from environment variables
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'messaging_product': 'whatsapp',
        'to': phone_number,
        'type': 'text',
        'text': {'body': message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending WhatsApp message: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == '__main__':
    print("Starting WhatsApp bot...")
    app.run(host='0.0.0.0', port=5000, debug=True)
