from database import db
from datetime import datetime, date
from sqlalchemy import func

class BudgetAnalytics:
    """Analytics and calculations for budget-related operations"""
    
    @staticmethod
    def calculate_budget_usage(user_id, category_id, start_date, end_date):
        """Calculate how much of budget has been used in a period"""
        from models import Transaction
        
        total_spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category_id == category_id,
            Transaction.type == 'expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).scalar() or 0.0
        
        return total_spent
    
    @staticmethod
    def get_budget_status(user_id, budget_id):
        """Get current status of a budget (remaining, percentage used, etc.)"""
        from models import Budget, Transaction
        
        budget = Budget.query.get(budget_id)
        if not budget or budget.user_id != user_id:
            return None
        
        spent = BudgetAnalytics.calculate_budget_usage(
            user_id, budget.category_id, budget.start_date, budget.end_date
        )
        
        remaining = budget.amount_limit - spent
        percentage_used = (spent / budget.amount_limit * 100) if budget.amount_limit > 0 else 0
        
        return {
            'budget_id': budget.id,
            'amount_limit': budget.amount_limit,
            'amount_spent': spent,
            'amount_remaining': remaining,
            'percentage_used': round(percentage_used, 2),
            'is_over_budget': spent > budget.amount_limit,
            'period': budget.period,
            'category_name': budget.category.name if budget.category else None
        }

class GoalCalculations:
    """Goal progress calculations and projections"""
    
    @staticmethod
    def calculate_goal_progress(goal_id):
        """Calculate detailed progress for a goal"""
        from models import Goal
        
        goal = Goal.query.get(goal_id)
        if not goal:
            return None
        
        progress_percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        remaining_amount = goal.target_amount - goal.current_amount
        
        # Calculate days remaining if target_date is set
        days_remaining = None
        daily_savings_needed = None
        
        if goal.target_date:
            days_remaining = (goal.target_date - date.today()).days
            if days_remaining > 0 and remaining_amount > 0:
                daily_savings_needed = remaining_amount / days_remaining
        
        return {
            'goal_id': goal.id,
            'title': goal.title,
            'target_amount': goal.target_amount,
            'current_amount': goal.current_amount,
            'remaining_amount': remaining_amount,
            'progress_percentage': round(progress_percentage, 2),
            'days_remaining': days_remaining,
            'daily_savings_needed': round(daily_savings_needed, 2) if daily_savings_needed else None,
            'is_completed': goal.current_amount >= goal.target_amount,
            'status': goal.status
        }
    
    @staticmethod
    def update_goal_progress(goal_id, amount_to_add):
        """Add amount to goal progress"""
        from models import Goal
        
        goal = Goal.query.get(goal_id)
        if not goal:
            return False
        
        goal.current_amount += amount_to_add
        
        # Auto-complete goal if target reached
        if goal.current_amount >= goal.target_amount:
            goal.status = 'completed'
        
        db.session.commit()
        return True

class RecurringTransactionProcessor:
    """Handle recurring transaction processing and scheduling"""
    
    @staticmethod
    def get_due_recurring_transactions(user_id=None):
        """Get all recurring transactions that are due"""
        from models import RecurringTransaction
        
        query = RecurringTransaction.query.filter(
            RecurringTransaction.is_active == True,
            RecurringTransaction.next_due_date <= date.today()
        )
        
        if user_id:
            query = query.filter(RecurringTransaction.user_id == user_id)
        
        return query.all()
    
    @staticmethod
    def process_recurring_transaction(recurring_id):
        """Process a recurring transaction (create actual transaction and update next due date)"""
        from models import RecurringTransaction, Transaction
        from dateutil.relativedelta import relativedelta
        
        recurring = RecurringTransaction.query.get(recurring_id)
        if not recurring or not recurring.is_active:
            return False
        
        # Create actual transaction
        transaction = Transaction(
            user_id=recurring.user_id,
            category_id=recurring.category_id,
            amount=recurring.amount,
            type=recurring.type,
            date=date.today(),
            note=f"Recurring: {recurring.description}" if recurring.description else "Recurring transaction"
        )
        
        db.session.add(transaction)
        
        # Update next due date based on frequency
        if recurring.frequency == 'daily':
            recurring.next_due_date += relativedelta(days=1)
        elif recurring.frequency == 'weekly':
            recurring.next_due_date += relativedelta(weeks=1)
        elif recurring.frequency == 'monthly':
            recurring.next_due_date += relativedelta(months=1)
        elif recurring.frequency == 'yearly':
            recurring.next_due_date += relativedelta(years=1)
        
        db.session.commit()
        return True
    
    @staticmethod
    def calculate_next_due_date(start_date, frequency):
        """Calculate the next due date for a recurring transaction"""
        from dateutil.relativedelta import relativedelta
        
        if frequency == 'daily':
            return start_date + relativedelta(days=1)
        elif frequency == 'weekly':
            return start_date + relativedelta(weeks=1)
        elif frequency == 'monthly':
            return start_date + relativedelta(months=1)
        elif frequency == 'yearly':
            return start_date + relativedelta(years=1)
        else:
            return start_date

class TransactionAnalytics:
    """Advanced transaction analytics and reporting"""
    
    @staticmethod
    def get_monthly_summary(user_id, year, month):
        """Get comprehensive monthly transaction summary"""
        from models import Transaction, Category
        from calendar import monthrange
        
        # Get first and last day of month
        start_date = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        end_date = date(year, month, last_day)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).all()
        
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
        net_amount = total_income - total_expenses
        
        # Category breakdown
        category_breakdown = {}
        for transaction in transactions:
            cat_name = transaction.category.name if transaction.category else 'Uncategorized'
            if cat_name not in category_breakdown:
                category_breakdown[cat_name] = {'income': 0, 'expense': 0, 'count': 0}
            category_breakdown[cat_name][transaction.type] += transaction.amount
            category_breakdown[cat_name]['count'] += 1
        
        return {
            'period': f"{year}-{month:02d}",
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_amount': net_amount,
            'transaction_count': len(transactions),
            'category_breakdown': category_breakdown,
            'average_daily_expense': total_expenses / last_day if total_expenses > 0 else 0
        }
    
    @staticmethod
    def get_spending_trends(user_id, months=6):
        """Get spending trends over the last N months"""
        from models import Transaction
        from dateutil.relativedelta import relativedelta
        
        end_date = date.today()
        start_date = end_date - relativedelta(months=months)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).order_by(Transaction.date).all()
        
        # Group by month
        monthly_data = {}
        for transaction in transactions:
            month_key = transaction.date.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = {'income': 0, 'expense': 0}
            monthly_data[month_key][transaction.type] += transaction.amount
        
        return monthly_data

class CategoryManager:
    """Advanced category management and operations"""
    
    @staticmethod
    def get_category_tree_with_totals(user_id, start_date=None, end_date=None):
        """Get category tree with transaction totals"""
        from models import Category, Transaction
        
        # Build transaction totals query
        query = Transaction.query.filter(Transaction.user_id == user_id)
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        transactions = query.all()
        
        # Calculate totals per category
        category_totals = {}
        for transaction in transactions:
            cat_id = transaction.category_id or 0  # 0 for uncategorized
            if cat_id not in category_totals:
                category_totals[cat_id] = {'income': 0, 'expense': 0, 'count': 0}
            category_totals[cat_id][transaction.type] += transaction.amount
            category_totals[cat_id]['count'] += 1
        
        # Get all categories
        categories = Category.query.all()
        
        # Build tree with totals
        category_tree = []
        parent_categories = [cat for cat in categories if cat.parent_id is None]
        
        for parent in parent_categories:
            parent_total = category_totals.get(parent.id, {'income': 0, 'expense': 0, 'count': 0})
            
            parent_data = {
                'id': parent.id,
                'name': parent.name,
                'parent_id': parent.parent_id,
                'totals': parent_total,
                'children': []
            }
            
            # Get children with totals
            children = [cat for cat in categories if cat.parent_id == parent.id]
            for child in children:
                child_total = category_totals.get(child.id, {'income': 0, 'expense': 0, 'count': 0})
                child_data = {
                    'id': child.id,
                    'name': child.name,
                    'parent_id': child.parent_id,
                    'totals': child_total
                }
                parent_data['children'].append(child_data)
                
                # Add child totals to parent
                parent_data['totals']['income'] += child_total['income']
                parent_data['totals']['expense'] += child_total['expense']
                parent_data['totals']['count'] += child_total['count']
            
            category_tree.append(parent_data)
        
        return category_tree
    
    @staticmethod
    def merge_categories(source_category_id, target_category_id):
        """Merge one category into another (move all transactions)"""
        from models import Category, Transaction, Budget, RecurringTransaction
        
        # Update all transactions
        Transaction.query.filter_by(category_id=source_category_id).update(
            {'category_id': target_category_id}
        )
        
        # Update all budgets
        Budget.query.filter_by(category_id=source_category_id).update(
            {'category_id': target_category_id}
        )
        
        # Update all recurring transactions
        RecurringTransaction.query.filter_by(category_id=source_category_id).update(
            {'category_id': target_category_id}
        )
        
        # Delete the source category
        Category.query.filter_by(id=source_category_id).delete()
        
        db.session.commit()
        return True

# Healthcheck for analytics (advanced, placeholder)
def healthcheck_analytics():
    try:
        from models import User, Category, Transaction, Budget, Goal, RecurringTransaction
        _ = [User, Category, Transaction, Budget, Goal, RecurringTransaction]
        return True
    except Exception:
        return False

