from flask import Flask, request, g  # type: ignore
from database import db   # import db from database.py
from models import User, Category, Transaction, Budget, Goal, RecurringTransaction  # import your models
import models_standard  # import advanced logic and analytics
# JWT imports temporarily removed for testing
# from flask_jwt_extended import JWTManager
from flasgger import Swagger
import logging
import time
import json
from datetime import datetime



app = Flask(__name__)

# JWT configuration temporarily disabled
# app.config['JWT_SECRET_KEY'] = '9512'  # change to env variable later
# app.config['JWT_IDENTITY_CLAIM'] = 'sub'

# ===== ENHANCED LOGGING CONFIGURATION =====
# Configure logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create custom logger for API requests
api_logger = logging.getLogger('budgetter_api')
api_logger.setLevel(logging.INFO)

# Console handler with custom formatting
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Custom formatter for better readability
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to log level
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

# Set custom formatter
formatter = ColoredFormatter(
    '%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
console_handler.setFormatter(formatter)
api_logger.addHandler(console_handler)

# Request logging middleware
@app.before_request
def log_request_info():
    """Log detailed information about incoming requests"""
    g.start_time = time.time()
    
    # Get request data
    method = request.method
    url = request.url
    remote_addr = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    content_type = request.headers.get('Content-Type', 'None')
    
    # Log request start
    api_logger.info(f"🔵 REQUEST START")
    api_logger.info(f"   Method: {method}")
    api_logger.info(f"   URL: {url}")
    api_logger.info(f"   IP: {remote_addr}")
    api_logger.info(f"   Content-Type: {content_type}")
    api_logger.info(f"   User-Agent: {user_agent[:50]}...")
    
    # Log request body for POST/PUT requests
    if method in ['POST', 'PUT', 'PATCH'] and request.is_json:
        try:
            body = request.get_json()
            if body:
                # Mask sensitive data
                safe_body = mask_sensitive_data(body)
                api_logger.info(f"   Body: {json.dumps(safe_body, indent=2)}")
        except Exception as e:
            api_logger.warning(f"   Body: Could not parse JSON - {str(e)}")

def mask_sensitive_data(data):
    """Mask sensitive fields in request/response data"""
    if not isinstance(data, dict):
        return data
    
    sensitive_fields = ['password', 'password_hash', 'current_password', 'new_password', 'access_token', 'refresh_token']
    masked_data = data.copy()
    
    for field in sensitive_fields:
        if field in masked_data:
            masked_data[field] = "***MASKED***"
    
    return masked_data

@app.after_request
def log_response_info(response):
    """Log detailed information about outgoing responses"""
    try:
        # Calculate request duration
        duration = round((time.time() - g.start_time) * 1000, 2)  # in milliseconds
        
        # Get response info
        status_code = response.status_code
        content_type = response.headers.get('Content-Type', 'Unknown')
        content_length = response.headers.get('Content-Length', 'Unknown')
        
        # Determine log level and emoji based on status code
        if 200 <= status_code < 300:
            log_level = 'info'
            emoji = "✅"
            status_text = "SUCCESS"
        elif 300 <= status_code < 400:
            log_level = 'info'
            emoji = "🔄"
            status_text = "REDIRECT"
        elif 400 <= status_code < 500:
            log_level = 'warning'
            emoji = "⚠️"
            status_text = "CLIENT ERROR"
        else:
            log_level = 'error'
            emoji = "❌"
            status_text = "SERVER ERROR"
        
        # Log response
        log_method = getattr(api_logger, log_level)
        log_method(f"{emoji} RESPONSE {status_text}")
        log_method(f"   Status: {status_code} {response.status}")
        log_method(f"   Duration: {duration}ms")
        log_method(f"   Content-Type: {content_type}")
        log_method(f"   Content-Length: {content_length}")
        
        # Log response body for JSON responses (truncated)
        if response.is_json and hasattr(response, 'get_json'):
            try:
                body = response.get_json()
                if body:
                    safe_body = mask_sensitive_data(body)
                    body_str = json.dumps(safe_body, indent=2)
                    # Truncate long responses
                    if len(body_str) > 500:
                        body_str = body_str[:500] + "... (truncated)"
                    log_method(f"   Response: {body_str}")
            except Exception:
                pass
        
        api_logger.info(f"🔵 REQUEST END - Total: {duration}ms")
        api_logger.info("=" * 80)
        
    except Exception as e:
        api_logger.error(f"Error in response logging: {str(e)}")
    
    return response

# Swagger configuration
swagger = Swagger(app)

# Configure the database (SQLite for now)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ bind db 
db.init_app(app)
# JWT manager temporarily disabled
# jwt = JWTManager(app)


# Import blueprints from new structure
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.category_routes import category_bp
from app.routes.transaction_routes import transaction_bp
from app.routes.budget_routes import budget_bp
from app.routes.goal_routes import goal_bp
from app.routes.recurring_routes import recurring_bp
from app.routes.health_route import health_bp
# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(category_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(budget_bp)
app.register_blueprint(goal_bp)
app.register_blueprint(recurring_bp)
app.register_blueprint(health_bp)

# Test route (keep it)
@app.route('/')
def home():
    return {'message': 'Budgetter API v1.0', 'status': 'active'}

if __name__ == '__main__':
    # Make sure tables exist before running
    with app.app_context():
        db.create_all()
    app.run(debug=True)
