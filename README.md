# Budgetter Backend API

A Flask-based REST API for budget management with SQLite database.

## 🏗️ Project Structure

```
Budgetter-backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # All 6 database models
│   ├── config.py                # Configuration settings
│   ├── utils.py                 # Helper functions
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py       # Authentication endpoints
│       ├── user_routes.py       # User management
│       ├── category_routes.py   # Category CRUD
│       ├── transaction_routes.py # Transaction management
│       ├── budget_routes.py     # Budget management
│       ├── goal_routes.py       # Financial goals
│       └── recurring_routes.py  # Recurring transactions
├── migrations/
│   ├── 001_create_users.sql
│   ├── 002_create_categories.sql
│   ├── 003_create_transactions.sql
│   ├── 004_create_budgets.sql
│   ├── 005_create_goals.sql
│   ├── 006_create_recurring_transactions.sql
│   └── run_migrations.py
├── postman/
│   └── collection.json          # Complete API collection
├── instance/
│   └── budget.db                # SQLite database
├── database.py                  # Database configuration
├── models.py                    # Main models file
├── run.py                       # Application entry point
└── requirements.txt             # Dependencies
```

## 📊 Database Schema (6 Tables)

1. **USERS** - User accounts and authentication
2. **CATEGORIES** - Budget categories with parent-child relationships
3. **TRANSACTIONS** - Income and expense records
4. **BUDGETS** - Monthly/yearly budget limits per category
5. **GOALS** - Financial savings goals
6. **RECURRING_TRANSACTIONS** - Scheduled recurring payments/income

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python run.py
```

The API will be available at `http://localhost:5000`

### 3. DataGrip Setup
1. Open DataGrip
2. Create New Data Source → SQLite
3. File: `c:\Users\Flutter-projects\Budgetter\Budgetter-backend\instance\budget.db`
4. Test Connection and Apply

### 4. Import Postman Collection
Import `postman/collection.json` into Postman for complete API testing.

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: `POST /api/auth/register`
2. **Login**: `POST /api/auth/login`
3. **Get Profile**: `GET /api/auth/me`
4. **Refresh Token**: `POST /api/auth/refresh`

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh access token

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `PUT /api/users/change-password` - Change password
- `DELETE /api/users/delete-account` - Delete account

### Categories
- `GET /api/categories/` - Get all categories (tree structure)
- `GET /api/categories/flat` - Get categories (flat list)
- `POST /api/categories/` - Create category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Transactions
- `GET /api/transactions/` - Get transactions (with pagination)
- `POST /api/transactions/` - Create transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction
- `GET /api/transactions/summary` - Get transaction summary

### Budgets
- `GET /api/budgets/` - Get user budgets
- `POST /api/budgets/` - Create budget

### Goals
- `GET /api/goals/` - Get financial goals
- `POST /api/goals/` - Create goal

### Recurring Transactions
- `GET /api/recurring-transactions/` - Get recurring transactions
- `POST /api/recurring-transactions/` - Create recurring transaction

## 🛠️ Development Tools

### Run Migrations
```bash
cd migrations
python run_migrations.py
```

### Verify Database
```bash
python verify_db.py
```

### Create Database
```bash
python create_db.py
```

## 📚 API Documentation

Swagger documentation is available at: `http://localhost:5000/apidocs`

## 🔧 Configuration

Environment variables can be set in `.env` file:
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `DATABASE_URL` - Database connection string

## 🧪 Testing

Use the Postman collection in `postman/collection.json` for comprehensive API testing. The collection includes:
- Authentication flow
- CRUD operations for all resources
- Error handling scenarios
- Pagination examples

## 📦 Dependencies

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flasgger** - Swagger documentation
- **SQLite** - Database

## 🎯 Features

- ✅ JWT Authentication
- ✅ User Management
- ✅ Category Management (hierarchical)
- ✅ Transaction Tracking
- ✅ Budget Management
- ✅ Financial Goals
- ✅ Recurring Transactions
- ✅ API Documentation
- ✅ Database Migrations
- ✅ Postman Collection
- ✅ DataGrip Integration
