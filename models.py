from database import db
from datetime import date

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

# Category model (with parent-child relationship)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return f"<Category {self.name}>"

# Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # "income" or "expense"
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    date = db.Column(db.Date, default=date.today)
    note = db.Column(db.String(200))

    # Relationships
    user = db.relationship('User', backref='transactions')
    category = db.relationship('Category', backref='transactions')

    def __repr__(self):
        return f"<Transaction {self.type} {self.amount}>"
