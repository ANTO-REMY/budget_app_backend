from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Transaction, Category
from app.utils import validate_amount, validate_date, success_response, error_response, require_json, paginate_query
from datetime import datetime, date

transaction_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transaction_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    """
    Get user transactions with pagination and filtering
    ---
    tags:
      - Transactions
    security:
      - Bearer: []
    responses:
      200:
        description: Transactions retrieved successfully
    """
    current_user_id = get_jwt_identity()
    
    # Build query
    query = Transaction.query.filter_by(user_id=current_user_id)
    
    # Apply filters
    transaction_type = request.args.get('type')
    if transaction_type in ['income', 'expense']:
        query = query.filter_by(type=transaction_type)
    
    category_id = request.args.get('category_id')
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Order by date (newest first)
    query = query.order_by(Transaction.date.desc(), Transaction.created_at.desc())
    
    # Paginate
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 20)
    
    paginated = paginate_query(query, page, per_page)
    if not paginated:
        return error_response("Invalid pagination parameters", 400)
    
    # Format transactions
    transactions_data = []
    for transaction in paginated['items']:
        transactions_data.append({
            'id': transaction.id,
            'amount': transaction.amount,
            'type': transaction.type,
            'category_id': transaction.category_id,
            'category_name': transaction.category.name if transaction.category else None,
            'date': transaction.date.isoformat() if transaction.date else None,
            'note': transaction.note,
            'created_at': transaction.created_at.isoformat() if transaction.created_at else None
        })
    
    return success_response({
        'transactions': transactions_data,
        'pagination': {
            'total': paginated['total'],
            'pages': paginated['pages'],
            'current_page': paginated['current_page'],
            'per_page': paginated['per_page'],
            'has_next': paginated['has_next'],
            'has_prev': paginated['has_prev']
        }
    })

@transaction_bp.route('/', methods=['POST'])
@jwt_required()
@require_json
def create_transaction():
    """
    Create a new transaction
    ---
    tags:
      - Transactions
    security:
      - Bearer: []
    responses:
      201:
        description: Transaction created successfully
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    amount = data.get('amount')
    transaction_type = data.get('type')
    
    if not amount or not transaction_type:
        return error_response("Amount and type are required", 400)
    
    # Validate amount
    is_valid, validated_amount = validate_amount(amount)
    if not is_valid:
        return error_response(validated_amount, 400)
    
    # Validate type
    if transaction_type not in ['income', 'expense']:
        return error_response("Type must be 'income' or 'expense'", 400)
    
    # Validate category if provided
    category_id = data.get('category_id')
    if category_id:
        category = Category.query.get(category_id)
        if not category:
            return error_response("Category not found", 400)
    
    # Validate date
    transaction_date = data.get('date')
    if transaction_date:
        transaction_date = validate_date(transaction_date)
        if not transaction_date:
            return error_response("Invalid date format. Use YYYY-MM-DD", 400)
    else:
        transaction_date = date.today()
    
    try:
        transaction = Transaction(
            user_id=current_user_id,
            amount=validated_amount,
            type=transaction_type,
            category_id=category_id,
            date=transaction_date,
            note=data.get('note', '').strip() or None
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return success_response({
            'transaction': {
                'id': transaction.id,
                'amount': transaction.amount,
                'type': transaction.type,
                'category_id': transaction.category_id,
                'category_name': transaction.category.name if transaction.category else None,
                'date': transaction.date.isoformat(),
                'note': transaction.note,
                'created_at': transaction.created_at.isoformat()
            }
        }, "Transaction created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create transaction", 500)
