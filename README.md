# BudgetAppProject
# Create backend folder (BudgetAppProject)
mkdir budget_app_backend
cd budget_app_backend

# Create virtual environment
python -m venv venv
# Activate it
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

# Install dependencies
pip install flask flask-restful flask-jwt-extended flask-cors sqlalchemy

# Save dependencies
pip freeze > requirements.txt

# Create main app file and run with
python app.py


