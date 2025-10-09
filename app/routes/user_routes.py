from flask import Blueprint, request
# JWT imports temporarily removed for testing
# from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User
from app.utils import validate_email, validate_password, success_response, error_response, require_json

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/profile', methods=['GET'])
# @jwt_required()  # Temporarily disabled
def get_profile():
    """
    Get user profile
    ---
    tags:
      - Users
    security:
      - Bearer: []
    responses:
      200:
        description: Profile retrieved successfully
      404:
        description: User not found
    """
    # current_user_id = get_jwt_identity()  # Temporarily disabled
    current_user_id = 1  # Default user for testing
    user = User.query.get(current_user_id)
    
    if not user:
        return error_response("User not found", 404)
    
    return success_response({
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }
    })

@user_bp.route('/profile', methods=['PUT'])
# @jwt_required()  # Temporarily disabled
@require_json
def update_profile():
    """
    Update user profile
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            first_name:
              type: string
              example: John
            last_name:
              type: string
              example: Doe
            email:
              type: string
              example: newemail@example.com
    responses:
      200:
        description: Profile updated successfully
      400:
        description: Validation error
      404:
        description: User not found
    """
    # current_user_id = get_jwt_identity()  # Temporarily disabled
    current_user_id = 1  # Default user for testing
    user = User.query.get(current_user_id)
    
    if not user:
        return error_response("User not found", 404)
    
    data = request.get_json()
    
    # Update fields if provided
    if 'first_name' in data:
        user.first_name = data['first_name'].strip() if data['first_name'] else None
    
    if 'last_name' in data:
        user.last_name = data['last_name'].strip() if data['last_name'] else None
    
    if 'email' in data:
        new_email = data['email'].strip().lower()
        if not validate_email(new_email):
            return error_response("Invalid email format", 400)
        
        # Check if email is already taken by another user
        existing_user = User.query.filter(User.email == new_email, User.id != user.id).first()
        if existing_user:
            return error_response("Email already taken", 400)
        
        user.email = new_email
    
    try:
        db.session.commit()
        return success_response({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
        }, "Profile updated successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update profile", 500)

@user_bp.route('/change-password', methods=['PUT'])
# @jwt_required()  # Temporarily disabled
@require_json
def change_password():
    """
    Change user password
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - current_password
            - new_password
          properties:
            current_password:
              type: string
              example: oldpassword123
            new_password:
              type: string
              example: newpassword123
    responses:
      200:
        description: Password changed successfully
      400:
        description: Validation error
      404:
        description: User not found
    """
    # current_user_id = get_jwt_identity()  # Temporarily disabled
    current_user_id = 1  # Default user for testing
    user = User.query.get(current_user_id)
    
    if not user:
        return error_response("User not found", 404)
    
    data = request.get_json()
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    
    if not current_password or not new_password:
        return error_response("Current password and new password are required", 400)
    
    # Verify current password
    if not check_password_hash(user.password_hash, current_password):
        return error_response("Current password is incorrect", 400)
    
    # Validate new password
    is_valid, message = validate_password(new_password)
    if not is_valid:
        return error_response(message, 400)
    
    try:
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return success_response(message="Password changed successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to change password", 500)

@user_bp.route('/delete-account', methods=['DELETE'])
# @jwt_required()  # Temporarily disabled
@require_json
def delete_account():
    """
    Delete user account
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - password
          properties:
            password:
              type: string
              example: password123
    responses:
      200:
        description: Account deleted successfully
      400:
        description: Validation error
      404:
        description: User not found
    """
    # current_user_id = get_jwt_identity()  # Temporarily disabled
    current_user_id = 1  # Default user for testing
    user = User.query.get(current_user_id)
    
    if not user:
        return error_response("User not found", 404)
    
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return error_response("Password is required to delete account", 400)
    
    # Verify password
    if not check_password_hash(user.password_hash, password):
        return error_response("Incorrect password", 400)
    
    try:
        # Delete user (cascade will handle related records)
        db.session.delete(user)
        db.session.commit()
        return success_response(message="Account deleted successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to delete account", 500)
