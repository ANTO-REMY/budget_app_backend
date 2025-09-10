# 📦 Budget App Backend (Flask)

This is the backend service for the **Budget App**.  
It provides authentication, transaction management, and summary APIs using **Flask + SQLite (MVP)**.  

---

## ⚙️ Setup Instructions

### 1. Install Python
Make sure you have **Python 3.10+** installed.  
Check version:
```bash
python --version
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```
Activate it:  
- Mac/Linux:
  ```bash
  source venv/bin/activate
  ```
- Windows:
  ```bash
  venv\Scripts\activate
  ```

### 3. Install Dependencies
```bash
pip install flask flask-restful flask-jwt-extended flask-cors sqlalchemy
```

### 4. Save Dependencies
```bash
pip freeze > requirements.txt
```

---

## ▶️ Running the App
Start the backend server:
```bash
python app.py
```

Visit in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)  
Expected output:
```
Hello, Budget App Backend!
```

---

## 📂 Project Structure
```
budget_app_backend/
│── app.py            # Entry point for Flask
│── models.py         # Database models (User, Transaction, Category)
│── routes.py         # API endpoints
│── database.py       # DB setup (SQLAlchemy)
│── requirements.txt  # Dependencies
```

---

## 🚀 Features (MVP)
- User signup/login (JWT authentication)  
- Add expenses/income  
- Categorize transactions  
- View monthly summaries  
- Export data (CSV/PDF) *(optional)*  

---

## 🧪 Testing
You can test API endpoints using **Postman** or **cURL**.  

Example:
```bash
curl http://127.0.0.1:5000/
```
