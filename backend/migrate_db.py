import sqlite3
import os

db_path = "test.db" # Standard path for this project's sqlite db

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(results)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if "matched_keywords" not in columns:
            print("Adding matched_keywords column to results table...")
            cursor.execute("ALTER TABLE results ADD COLUMN matched_keywords TEXT")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column matched_keywords already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")
else:
    print(f"Database file {db_path} not found. SQLAlchemy will create it automatically with the new schema.")
