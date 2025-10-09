from functools import wraps
from flask import jsonify, request
# JWT imports temporarily removed for testing
# from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"

def validate_amount(amount):
    """Validate monetary amount"""
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than 0"
        return True, amount
    except (ValueError, TypeError):
        return False, "Invalid amount format"

def validate_date(date_string):
    """Validate date format (YYYY-MM-DD)"""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None

def success_response(data=None, message="Success", status_code=200):
    """Standard success response format"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    """Standard error response format"""
    response = {
        'success': False,
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code

def paginate_query(query, page=1, per_page=20):
    """Paginate SQLAlchemy query"""
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else 20
        per_page = min(per_page, 100)  # Max 100 items per page
        
        paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    except Exception as e:
        return None

def require_json(f):
    """Decorator to ensure request contains JSON data"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return error_response("Request must contain JSON data", 400)
        return f(*args, **kwargs)
    return decorated_function

def get_current_user_id():
    """Get current authenticated user ID from JWT (temporarily disabled)"""
    # return get_jwt_identity()  # Temporarily disabled
    return 1  # Default user for testing

class DateTimeEncoder:
    """Helper class for JSON serialization of datetime objects"""
    
    @staticmethod
    def serialize_datetime(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        return obj
