import sqlite3

DB_PATH = "eduevalve.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE results ADD COLUMN explainable_output TEXT")
    print("✅ Column explainable_output added successfully!")
except Exception as e:
    print("⚠️ Column already exists OR error:", e)

conn.commit()
conn.close()
