from flask import Blueprint, request, jsonify
from config.database import get_pg_connection
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email'), data.get('password')
    conn = get_pg_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, role FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    
    if user:
        token = request.app.config['API_TOKEN']
        cursor.execute("INSERT INTO audit_logs (user_id, action, timestamp) VALUES (%s, %s, %s)",
                       (user[0], 'login', datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'api_token': token, 'user_id': user[0]}), 200
    
    cursor.close()
    conn.close()
    return jsonify({'error': 'Invalid credentials'}), 401