from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Transaction
from datetime import datetime   

# Create blueprint
transactions_bp = Blueprint('transactions', __name__)

# GET /transactions → fetch all transactions for current user
@transactions_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """
    Get Transactions
    ---
    tags:
      - Transactions
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of all transactions for the current user
      401:
        description: Unauthorized (JWT missing/invalid)
    """
    # ✅ Get the logged-in user's ID from the JWT
    user_id = int(get_jwt_identity())

    # ✅ Query transactions belonging to that user
    transactions = Transaction.query.filter_by(user_id=user.id).all()

    # Convert results to list of dictionaries
    result = []
    for t in transactions:
        result.append({
            "id": t.id,
            "amount": t.amount,
            "type": t.type,
            "category_id": t.category_id,
            "date": t.date.isoformat() if t.date else None,
            "note": t.note
        })

    return jsonify(result), 200

def new_func():
    user_id = get_jwt_identity()
    return user_id


# POST /transactions → create a new transaction
@transactions_bp.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    """
    Create Transaction
    ---
    tags:
      - Transactions
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            amount:
              type: number
              example: 1500
            type:
              type: string
              enum: [income, expense]
              example: expense
            category_id:
              type: integer
              example: 2
            date:
              type: string
              format: date
              example: 2025-09-10
            note:
              type: string
              example: Bought groceries
    responses:
      201:
        description: Transaction added successfully
      400:
        description: Invalid input
      401:
        description: Unauthorized (JWT missing/invalid)
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    new_transaction = Transaction(
        user_id=user_id,
        amount=data['amount'],
        type=data['type'],  # "income" or "expense"
        category_id=data['category_id'],
        date=datetime.strptime(data['date'], "%Y-%m-%d").date(),  # ✅ convert to Python date
        note=data.get('note', "")
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully!"}), 201
