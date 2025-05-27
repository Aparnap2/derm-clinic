from flask import Blueprint, request, jsonify
from config.database import get_pg_connection
from config.agent.adk import get_patient_agent
from utils.whatsapp import send_whatsapp_message
from datetime import datetime

whatsapp_bp = Blueprint('whatsapp', __name__)

@whatsapp_bp.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    data = request.json
    if data['object'] == 'whatsapp_business_account':
        for entry in data['entry']:
            for change in entry['changes']:
                if change['field'] == 'messages':
                    message = change['value']['messages'][0]
                    phone_number = message['from']
                    text = message['text']['body']
                    
                    agent = get_patient_agent()
                    response = agent.run(text)
                    
                    send_whatsapp_message(phone_number, response)
                    
                    conn = get_pg_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO messages (phone_number, message, response, timestamp) VALUES (%s, %s, %s, %s)",
                                   (phone_number, text, response, datetime.now()))
                    conn.commit()
                    cursor.close()
                    conn.close()
    
    return jsonify({'status': 'success'}), 200

@whatsapp_bp.route('/whatsapp/verify', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == 'your-verify-token':
        return challenge, 200
    return jsonify({'error': 'Verification failed'}), 403