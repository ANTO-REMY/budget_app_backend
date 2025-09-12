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
## 📦 Install Flask-SQLAlchemy

Run this in your terminal:

```bash
pip install flask flask_sqlalchemy
pip install flask-jwt-extended # for authentication


# 🗂 How to Access SQLite Database Files (`budget.db`)

Your database file (`budget.db`) is **binary** and cannot be opened in a text editor.  
Here are ways to explore and inspect it:

---

## 1. 🛠 SQLite Command-Line Tool

If you have `sqlite3` installed, run:

```bash
sqlite3 budget.db
```

Inside the shell, you can run:

```sql
.tables             -- list all tables
.schema users       -- show table structure of the 'users' table
SELECT * FROM users;  -- view all data in the 'users' table
```

Exit the SQLite shell with:

```sql
.quit
```

---

## 2. 📊 DB Browser for SQLite (Beginner Friendly)

- Download: [https://sqlitebrowser.org](https://sqlitebrowser.org)  
- Open `budget.db` → browse tables like `user`, `category`, `transaction`  
- Run queries or edit data in a **GUI interface**  

---

## 3. 🐍 View Data Inside Python (Flask Context)

Open a Python shell in your project folder and run:

```python
from app import app
from database import db
from models import User, Category, Transaction

with app.app_context():
    print(User.query.all())         # view all users
    print(Category.query.all())     # view all categories
    print(Transaction.query.all())  # view all transactions
```

---

## 📌 Concept Note: **Database Viewer**

- A `SQLite database` is stored in a single `.db` file.  
- It is **not human-readable** in a text editor.  
- To explore it, always use a **Database Viewer** like:
  - `sqlite3` CLI  
  - DB Browser for SQLite  
  - Queries inside Python/Flask

# 🛠 How to Install SQLite (`sqlite3`)

SQLite is a lightweight database engine that comes with the command-line tool `sqlite3`.  
Follow the instructions for your operating system.

---

## 1. Windows

1. Go to the SQLite download page: [https://www.sqlite.org/download.html](https://www.sqlite.org/download.html)  
2. Download the **"sqlite-tools-win32-x64-xxxx.zip"** file (contains `sqlite3.exe`).  
3. Extract the ZIP file to a folder (e.g., `C:\sqlite`).  
4. Add the folder to your **PATH environment variable** so you can run `sqlite3` from any command prompt:
   - Press **Win + S**, search for **Environment Variables**, open **Edit system environment variables**  
   - Click **Environment Variables → Path → Edit → New**, add `C:\sqlite`  
   - Click OK  
5. Open a new Command Prompt and run:
   ```bash
   sqlite3 --version

## 📦 Install flasgger
pip install flasgger