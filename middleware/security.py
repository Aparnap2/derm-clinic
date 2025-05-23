from flask import request, jsonify
from functools import wraps
import re

def require_api_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-API-Token')
        if not token or token != request.app.config['API_TOKEN']:
            return jsonify({'error': 'Invalid or missing API token'}), 401
        return f(*args, **kwargs)
    return decorated

def sanitize_input(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.json or {}
        for key, value in data.items():
            if isinstance(value, str):
                if re.search(r'[<>{};]', value):
                    return jsonify({'error': 'Invalid input', 'message': 'Suspicious characters detected'}), 400
        return f(*args, **kwargs)
    return decorated

def init_security(app):
    for endpoint, func in app.view_functions.items():
        if endpoint not in ['whatsapp_webhook', 'verify_webhook', 'login']:
            app.view_functions[endpoint] = require_api_token(sanitize_input(func))