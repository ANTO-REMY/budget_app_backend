from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Transaction

# Create blueprint
transactions_bp = Blueprint('transactions', __name__)

# GET /transactions → fetch all transactions for current user
@transactions_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()  # get logged-in user ID from JWT
    transactions = Transaction.query.filter_by(user_id=user_id).all()

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


# POST /transactions → create a new transaction
@transactions_bp.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_transaction = Transaction(
        user_id=user_id,
        amount=data['amount'],
        type=data['type'],  # "income" or "expense"
        category_id=data['category_id'],
        date=data['date'],  # string e.g. "2025-09-10"
        note=data.get('note', "")
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully!"}), 201
