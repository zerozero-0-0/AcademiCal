import sqlite3
from src.database.DB_name import DB_name

def DB_Connect():
    conn = sqlite3.connect(DB_name, isolation_level=None, timeout=10)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT CHECK(status IN ('pending','completed')) DEFAULT 'pending')            
    """)

    conn.commit()
    cursor.close()
    conn.close()
