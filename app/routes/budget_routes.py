from flask import Blueprint, request
# JWT imports temporarily removed for testing
# from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Budget, Category
from app.utils import validate_amount, validate_date, success_response, error_response, require_json
from datetime import datetime, date

budget_bp = Blueprint('budgets', __name__, url_prefix='/api/budgets')

@budget_bp.route('/', methods=['GET'])
# @jwt_required()  # Temporarily disabled
def get_budgets():
    """
    Get user budgets
    ---
    tags:
      - Budgets
    security:
      - Bearer: []
    responses:
      200:
        description: Budgets retrieved successfully
    """
    # current_user_id = get_jwt_identity()  # Temporarily disabled
    current_user_id = 1  # Default user for testing
    
    budgets = Budget.query.filter_by(user_id=current_user_id).all()
    
    budgets_data = []
    for budget in budgets:
        budgets_data.append({
            'id': budget.id,
            'category_id': budget.category_id,
            'category_name': budget.category.name if budget.category else None,
            'amount_limit': budget.amount_limit,
            'period': budget.period,
            'start_date': budget.start_date.isoformat(),
            'end_date': budget.end_date.isoformat(),
            'created_at': budget.created_at.isoformat() if budget.created_at else None
        })
    
    return success_response({
        'budgets': budgets_data,
        'total': len(budgets)
    })

@budget_bp.route('/', methods=['POST'])
# @jwt_required()  # Temporarily disabled
@require_json
def create_budget():
    """
    Create a new budget
    ---
    tags:
      - Budgets
    security:
      - Bearer: []
    responses:
      201:
        description: Budget created successfully
    """
    # current_user_id = get_jwt_identity()  # Temporarily disabled
    current_user_id = 1  # Default user for testing
    data = request.get_json()
    
    # Validate required fields
    category_id = data.get('category_id')
    amount_limit = data.get('amount_limit')
    period = data.get('period')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if not all([category_id, amount_limit, period, start_date, end_date]):
        return error_response("All fields are required: category_id, amount_limit, period, start_date, end_date", 400)
    
    # Validate category
    category = Category.query.get(category_id)
    if not category:
        return error_response("Category not found", 400)
    
    # Validate amount
    is_valid, validated_amount = validate_amount(amount_limit)
    if not is_valid:
        return error_response(validated_amount, 400)
    
    # Validate period
    if period not in ['monthly', 'yearly']:
        return error_response("Period must be 'monthly' or 'yearly'", 400)
    
    # Validate dates
    start_date = validate_date(start_date)
    end_date = validate_date(end_date)
    
    if not start_date or not end_date:
        return error_response("Invalid date format. Use YYYY-MM-DD", 400)
    
    if end_date <= start_date:
        return error_response("End date must be after start date", 400)
    
    # Check for existing budget for same category and period
    existing_budget = Budget.query.filter_by(
        user_id=current_user_id,
        category_id=category_id,
        period=period,
        start_date=start_date
    ).first()
    
    if existing_budget:
        return error_response("Budget already exists for this category and period", 400)
    
    try:
        budget = Budget(
            user_id=current_user_id,
            category_id=category_id,
            amount_limit=validated_amount,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(budget)
        db.session.commit()
        
        return success_response({
            'budget': {
                'id': budget.id,
                'category_id': budget.category_id,
                'category_name': budget.category.name,
                'amount_limit': budget.amount_limit,
                'period': budget.period,
                'start_date': budget.start_date.isoformat(),
                'end_date': budget.end_date.isoformat(),
                'created_at': budget.created_at.isoformat()
            }
        }, "Budget created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create budget", 500)
