#!/usr/bin/env python3
"""
Script to create a test user for testing endpoints without authentication
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app from app.py
import app as app_module
app = app_module.app
from database import db
from models import User
from werkzeug.security import generate_password_hash

def create_test_user():
    """Create a test user with ID 1 if it doesn't exist"""
    with app.app_context():
        # Check if user with ID 1 already exists
        existing_user = User.query.get(1)
        
        if existing_user:
            print(f"Test user already exists: {existing_user.email}")
            return existing_user
        
        # Create test user
        test_user = User(
            email="test@example.com",
            password_hash=generate_password_hash("password123"),
            first_name="Test",
            last_name="User"
        )
        
        try:
            db.session.add(test_user)
            db.session.commit()
            print(f"Created test user: {test_user.email} (ID: {test_user.id})")
            return test_user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating test user: {e}")
            return None

if __name__ == "__main__":
    create_test_user()
