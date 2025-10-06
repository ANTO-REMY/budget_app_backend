from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Category
from app.utils import success_response, error_response, require_json

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Get all categories
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    responses:
      200:
        description: Categories retrieved successfully
    """
    try:
        categories = Category.query.all()
        
        # Organize categories with parent-child relationships
        category_tree = []
        parent_categories = [cat for cat in categories if cat.parent_id is None]
        
        for parent in parent_categories:
            parent_data = {
                'id': parent.id,
                'name': parent.name,
                'parent_id': parent.parent_id,
                'children': []
            }
            
            # Get children
            children = [cat for cat in categories if cat.parent_id == parent.id]
            for child in children:
                child_data = {
                    'id': child.id,
                    'name': child.name,
                    'parent_id': child.parent_id
                }
                parent_data['children'].append(child_data)
            
            category_tree.append(parent_data)
        
        return success_response({
            'categories': category_tree,
            'total': len(categories)
        })
    
    except Exception as e:
        return error_response("Failed to retrieve categories", 500)

@category_bp.route('/flat', methods=['GET'])
@jwt_required()
def get_categories_flat():
    """
    Get all categories as flat list
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    responses:
      200:
        description: Categories retrieved successfully
    """
    try:
        categories = Category.query.all()
        
        categories_data = []
        for category in categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'parent_id': category.parent_id,
                'parent_name': category.parent.name if category.parent else None
            })
        
        return success_response({
            'categories': categories_data,
            'total': len(categories)
        })
    
    except Exception as e:
        return error_response("Failed to retrieve categories", 500)

@category_bp.route('/', methods=['POST'])
@jwt_required()
@require_json
def create_category():
    """
    Create a new category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: New Category
            parent_id:
              type: integer
              example: 1
    responses:
      201:
        description: Category created successfully
      400:
        description: Validation error
    """
    data = request.get_json()
    
    name = data.get('name', '').strip()
    parent_id = data.get('parent_id')
    
    if not name:
        return error_response("Category name is required", 400)
    
    # Check if category name already exists at the same level
    existing_query = Category.query.filter_by(name=name, parent_id=parent_id)
    if existing_query.first():
        return error_response("Category with this name already exists at this level", 400)
    
    # Validate parent category exists if parent_id is provided
    if parent_id:
        parent_category = Category.query.get(parent_id)
        if not parent_category:
            return error_response("Parent category not found", 400)
    
    try:
        category = Category(
            name=name,
            parent_id=parent_id
        )
        
        db.session.add(category)
        db.session.commit()
        
        return success_response({
            'category': {
                'id': category.id,
                'name': category.name,
                'parent_id': category.parent_id,
                'parent_name': category.parent.name if category.parent else None
            }
        }, "Category created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create category", 500)

@category_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
@require_json
def update_category(category_id):
    """
    Update a category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - in: path
        name: category_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
              example: Updated Category
            parent_id:
              type: integer
              example: 2
    responses:
      200:
        description: Category updated successfully
      404:
        description: Category not found
      400:
        description: Validation error
    """
    category = Category.query.get(category_id)
    if not category:
        return error_response("Category not found", 404)
    
    data = request.get_json()
    
    if 'name' in data:
        new_name = data['name'].strip()
        if not new_name:
            return error_response("Category name cannot be empty", 400)
        
        # Check for duplicate names at the same level (excluding current category)
        existing = Category.query.filter(
            Category.name == new_name,
            Category.parent_id == category.parent_id,
            Category.id != category_id
        ).first()
        
        if existing:
            return error_response("Category with this name already exists at this level", 400)
        
        category.name = new_name
    
    if 'parent_id' in data:
        parent_id = data['parent_id']
        
        # Prevent setting parent to self or descendant
        if parent_id == category_id:
            return error_response("Category cannot be its own parent", 400)
        
        if parent_id:
            parent_category = Category.query.get(parent_id)
            if not parent_category:
                return error_response("Parent category not found", 400)
        
        category.parent_id = parent_id
    
    try:
        db.session.commit()
        return success_response({
            'category': {
                'id': category.id,
                'name': category.name,
                'parent_id': category.parent_id,
                'parent_name': category.parent.name if category.parent else None
            }
        }, "Category updated successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update category", 500)

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """
    Delete a category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    parameters:
      - in: path
        name: category_id
        type: integer
        required: true
    responses:
      200:
        description: Category deleted successfully
      404:
        description: Category not found
      400:
        description: Cannot delete category with children or transactions
    """
    category = Category.query.get(category_id)
    if not category:
        return error_response("Category not found", 404)
    
    # Check if category has children
    children = Category.query.filter_by(parent_id=category_id).first()
    if children:
        return error_response("Cannot delete category that has subcategories", 400)
    
    # Check if category has transactions
    if category.transactions:
        return error_response("Cannot delete category that has transactions", 400)
    
    # Check if category has budgets
    if category.budgets:
        return error_response("Cannot delete category that has budgets", 400)
    
    try:
        db.session.delete(category)
        db.session.commit()
        return success_response(message="Category deleted successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to delete category", 500)
