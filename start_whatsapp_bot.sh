#!/bin/bash

# Start ngrok in the background
echo "Starting ngrok..."
ngrok http 5000 > /dev/null &

# Give ngrok a few seconds to start
sleep 5

# Get the public URL from ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [ -z "$NGROK_URL" ]; then
    echo "Failed to get ngrok URL. Make sure ngrok is installed and authenticated."
    exit 1
fi

echo "Ngrok URL: $NGROK_URL"
echo "Update your WhatsApp webhook URL in Meta Developer Console to: $NGROK_URL"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install requirements if not already installed
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Start the WhatsApp bot
echo "Starting WhatsApp bot..."
python3 whatsapp_bot.py

# Cleanup function to stop background processes
cleanup() {
    echo "Stopping ngrok..."
    pkill -f ngrok
    exit 0
}

# Set trap to catch script termination
trap cleanup SIGINT SIGTERM

# Keep script running
wait
