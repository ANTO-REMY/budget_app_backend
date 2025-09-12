from flask import Flask  # type: ignore
from database import db   # import db from database.py
from models import User, Category, Transaction  # import your models
from flask_jwt_extended import JWTManager
from flasgger import Swagger



app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = '9512'  # change to env variable later
jwt = JWTManager(app)
app.config['JWT_IDENTITY_CLAIM'] = 'sub'


# Swagger configuration
swagger = Swagger(app)

# Configure the database (SQLite for now)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ bind db 
db.init_app(app)
jwt = JWTManager(app)


# Import blueprints
from routes.auth import auth_bp
app.register_blueprint(auth_bp)

from routes.transactions import transactions_bp
app.register_blueprint(transactions_bp)


# Test route (keep it)
@app.route('/')
def home():
    return 'Hello, Budget App Backend!'

if __name__ == '__main__':
    # Make sure tables exist before running
    with app.app_context():
        db.create_all()
    app.run(debug=True)
