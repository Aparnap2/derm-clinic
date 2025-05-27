import requests
import os
from config.agent.adk import get_patient_agent

WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/652573494605608/messages"
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')

def send_whatsapp_message(to: str, body: str):
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {
        'messaging_product': 'whatsapp',
        'to': to,
        'type': 'text',
        'text': {'body': body}
    }
    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    return response.json()

def configure_webhook():
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "652573494605608",
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "webhook": "https://your-api-domain.com/api/whatsapp",
                            "verify_token": "your-verify-token"
                        }
                    }
                ]
            }
        ]
    }
    response = requests.post(
        "https://graph.facebook.com/v22.0/652573494605608/subscriptions",
        json=payload,
        headers=headers
    )
    return response.json()