from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import RecurringTransaction, Category
from app.utils import validate_amount, validate_date, success_response, error_response, require_json

recurring_bp = Blueprint('recurring', __name__, url_prefix='/api/recurring-transactions')

@recurring_bp.route('/', methods=['GET'])
@jwt_required()
def get_recurring_transactions():
    """
    Get user recurring transactions
    ---
    tags:
      - Recurring Transactions
    security:
      - Bearer: []
    responses:
      200:
        description: Recurring transactions retrieved successfully
    """
    current_user_id = get_jwt_identity()
    
    recurring_transactions = RecurringTransaction.query.filter_by(user_id=current_user_id).all()
    
    transactions_data = []
    for transaction in recurring_transactions:
        transactions_data.append({
            'id': transaction.id,
            'category_id': transaction.category_id,
            'category_name': transaction.category.name if transaction.category else None,
            'amount': transaction.amount,
            'type': transaction.type,
            'frequency': transaction.frequency,
            'next_due_date': transaction.next_due_date.isoformat(),
            'is_active': transaction.is_active,
            'description': transaction.description,
            'created_at': transaction.created_at.isoformat() if transaction.created_at else None
        })
    
    return success_response({
        'recurring_transactions': transactions_data,
        'total': len(recurring_transactions)
    })

@recurring_bp.route('/', methods=['POST'])
@jwt_required()
@require_json
def create_recurring_transaction():
    """
    Create a new recurring transaction
    ---
    tags:
      - Recurring Transactions
    security:
      - Bearer: []
    responses:
      201:
        description: Recurring transaction created successfully
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    category_id = data.get('category_id')
    amount = data.get('amount')
    transaction_type = data.get('type')
    frequency = data.get('frequency')
    next_due_date = data.get('next_due_date')
    
    if not all([category_id, amount, transaction_type, frequency, next_due_date]):
        return error_response("All fields are required: category_id, amount, type, frequency, next_due_date", 400)
    
    # Validate category
    category = Category.query.get(category_id)
    if not category:
        return error_response("Category not found", 400)
    
    # Validate amount
    is_valid, validated_amount = validate_amount(amount)
    if not is_valid:
        return error_response(validated_amount, 400)
    
    # Validate type
    if transaction_type not in ['income', 'expense']:
        return error_response("Type must be 'income' or 'expense'", 400)
    
    # Validate frequency
    if frequency not in ['daily', 'weekly', 'monthly', 'yearly']:
        return error_response("Frequency must be 'daily', 'weekly', 'monthly', or 'yearly'", 400)
    
    # Validate date
    next_due_date = validate_date(next_due_date)
    if not next_due_date:
        return error_response("Invalid date format. Use YYYY-MM-DD", 400)
    
    try:
        recurring_transaction = RecurringTransaction(
            user_id=current_user_id,
            category_id=category_id,
            amount=validated_amount,
            type=transaction_type,
            frequency=frequency,
            next_due_date=next_due_date,
            is_active=data.get('is_active', True),
            description=data.get('description', '').strip() or None
        )
        
        db.session.add(recurring_transaction)
        db.session.commit()
        
        return success_response({
            'recurring_transaction': {
                'id': recurring_transaction.id,
                'category_id': recurring_transaction.category_id,
                'category_name': recurring_transaction.category.name,
                'amount': recurring_transaction.amount,
                'type': recurring_transaction.type,
                'frequency': recurring_transaction.frequency,
                'next_due_date': recurring_transaction.next_due_date.isoformat(),
                'is_active': recurring_transaction.is_active,
                'description': recurring_transaction.description,
                'created_at': recurring_transaction.created_at.isoformat()
            }
        }, "Recurring transaction created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create recurring transaction", 500)
