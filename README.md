# WhatsApp Bot for Dermatology Clinic

A WhatsApp Business API integration that provides automated responses to patient queries using AI.

## Prerequisites

- Python 3.8+
- ngrok (for local development)
- WhatsApp Business Account
- Meta Developer Account with WhatsApp Business API access

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd derm-clinic-backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your credentials:
   ```
   VERIFY_TOKEN=your_verify_token
   WHATSAPP_TOKEN=your_whatsapp_token
   WHATSAPP_PHONE=your_whatsapp_phone_id
   WHATSAPP_API_URL=https://graph.facebook.com/v22.0/YOUR_PHONE_ID/messages
   ```

## Running the Bot

1. **Make the startup script executable**
   ```bash
   chmod +x start_whatsapp_bot.sh
   ```

2. **Start the bot**
   ```bash
   ./start_whatsapp_bot.sh
   ```

3. **Set up webhook**
   - The script will display an ngrok URL
   - Go to your [Meta Developer Dashboard](https://developers.facebook.com/apps/)
   - Navigate to WhatsApp → Configuration → Webhook
   - Set the Callback URL to your ngrok URL
   - Set Verify Token to match your `VERIFY_TOKEN` in `.env`
   - Subscribe to these fields:
     - messages
     - message_template_status_update

## Development

- Main bot logic: `whatsapp_bot.py`
- AI agent implementation: `agent/agent.py`
- Configuration: `config/ai_config.py`

## Environment Variables

- `VERIFY_TOKEN`: Token for webhook verification
- `WHATSAPP_TOKEN`: Your WhatsApp Business API token
- `WHATSAPP_PHONE`: Your WhatsApp Business phone number ID
- `WHATSAPP_API_URL`: WhatsApp API endpoint URL

## Troubleshooting

- **Webhook verification fails**: Ensure the verify token matches exactly
- **401 Unauthorized**: Check if your WhatsApp token is valid and not expired
- **404 Not Found**: Make sure the webhook URL is correct and the server is running

## License

This project is licensed under the MIT License.
