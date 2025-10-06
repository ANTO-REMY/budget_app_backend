import sqlite3
import os
from pathlib import Path

def run_migrations():
    """Run all SQL migration files in order"""
    
    # Database path
    db_path = Path(__file__).parent.parent / "instance" / "budget.db"
    migrations_dir = Path(__file__).parent
    
    # Get all migration files in order
    migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
    
    if not migration_files:
        print("❌ No migration files found!")
        return
    
    print("🚀 Running Database Migrations...")
    print("=" * 50)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        for migration_file in migration_files:
            print(f"📄 Running: {migration_file}")
            
            # Read migration file
            with open(migrations_dir / migration_file, 'r') as f:
                sql_content = f.read()
            
            # Execute SQL commands
            cursor.executescript(sql_content)
            print(f"✅ Completed: {migration_file}")
        
        # Commit all changes
        conn.commit()
        print("\n🎉 All migrations completed successfully!")
        
        # Show table count
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📊 Total tables: {len(tables)}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    run_migrations()
