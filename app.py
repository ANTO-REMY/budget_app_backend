from flask import Flask  # type: ignore
from database import db   # import db from database.py
from models import User, Category, Transaction, Budget, Goal, RecurringTransaction  # import your models
import models_standard  # import advanced logic and analytics
from flask_jwt_extended import JWTManager
from flasgger import Swagger



app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = '9512'  # change to env variable later
app.config['JWT_IDENTITY_CLAIM'] = 'sub'


# Swagger configuration
swagger = Swagger(app)

# Configure the database (SQLite for now)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ bind db 
db.init_app(app)
jwt = JWTManager(app)


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
