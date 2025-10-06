# Budgetter Backend API

A Flask-based REST API for budget management with SQLite database.

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
