from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from middleware.error_handler import init_error_handlers
from middleware.security import init_security
from routes.auth import auth_bp
from routes.rag import rag_bp
from routes.upload import upload_bp
from routes.analytics import analytics_bp
from routes.whatsapp import whatsapp_bp
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
jwt = JWTManager(app)

# Initialize middleware
init_error_handlers(app)
init_security(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(rag_bp, url_prefix='/api')
app.register_blueprint(upload_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')
app.register_blueprint(whatsapp_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(ssl_context='adhoc', host='0.0.0.0', port=443)