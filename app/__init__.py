from flask import Flask
from database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = '9512'  # TODO: Move to environment variable
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    swagger = Swagger(app)
    
    # Import models to ensure they're registered
    from models import User, Category, Transaction, Budget, Goal, RecurringTransaction
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.category_routes import category_bp
    from app.routes.transaction_routes import transaction_bp
    from app.routes.budget_routes import budget_bp
    from app.routes.goal_routes import goal_bp
    from app.routes.recurring_routes import recurring_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(goal_bp)
    app.register_blueprint(recurring_bp)
    
    # Test route
    @app.route('/')
    def home():
        return {'message': 'Budgetter API v1.0', 'status': 'active'}
    
    return app
