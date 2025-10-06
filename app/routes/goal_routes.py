from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Goal
from app.utils import validate_amount, validate_date, success_response, error_response, require_json

goal_bp = Blueprint('goals', __name__, url_prefix='/api/goals')

@goal_bp.route('/', methods=['GET'])
@jwt_required()
def get_goals():
    """
    Get user goals
    ---
    tags:
      - Goals
    security:
      - Bearer: []
    responses:
      200:
        description: Goals retrieved successfully
    """
    current_user_id = get_jwt_identity()
    
    goals = Goal.query.filter_by(user_id=current_user_id).all()
    
    goals_data = []
    for goal in goals:
        progress_percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        
        goals_data.append({
            'id': goal.id,
            'title': goal.title,
            'target_amount': goal.target_amount,
            'current_amount': goal.current_amount,
            'progress_percentage': round(progress_percentage, 2),
            'target_date': goal.target_date.isoformat() if goal.target_date else None,
            'status': goal.status,
            'created_at': goal.created_at.isoformat() if goal.created_at else None
        })
    
    return success_response({
        'goals': goals_data,
        'total': len(goals)
    })

@goal_bp.route('/', methods=['POST'])
@jwt_required()
@require_json
def create_goal():
    """
    Create a new goal
    ---
    tags:
      - Goals
    security:
      - Bearer: []
    responses:
      201:
        description: Goal created successfully
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    title = data.get('title', '').strip()
    target_amount = data.get('target_amount')
    
    if not title or not target_amount:
        return error_response("Title and target_amount are required", 400)
    
    # Validate amount
    is_valid, validated_amount = validate_amount(target_amount)
    if not is_valid:
        return error_response(validated_amount, 400)
    
    # Validate target date if provided
    target_date = data.get('target_date')
    if target_date:
        target_date = validate_date(target_date)
        if not target_date:
            return error_response("Invalid date format. Use YYYY-MM-DD", 400)
    
    try:
        goal = Goal(
            user_id=current_user_id,
            title=title,
            target_amount=validated_amount,
            current_amount=data.get('current_amount', 0.0),
            target_date=target_date,
            status=data.get('status', 'active')
        )
        
        db.session.add(goal)
        db.session.commit()
        
        progress_percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        
        return success_response({
            'goal': {
                'id': goal.id,
                'title': goal.title,
                'target_amount': goal.target_amount,
                'current_amount': goal.current_amount,
                'progress_percentage': round(progress_percentage, 2),
                'target_date': goal.target_date.isoformat() if goal.target_date else None,
                'status': goal.status,
                'created_at': goal.created_at.isoformat()
            }
        }, "Goal created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create goal", 500)
