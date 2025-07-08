import sqlite3

def DB_Connect():
    
    DB_name = 'assignment.db'
    conn = sqlite3.connect(DB_name, isolation_level=None)
    
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT CHECK(status IN ('pending', 'completed')) DEFAULT 'pending',
        )            
    ''')
    
    cursor.close()
    conn.close()
    
    
