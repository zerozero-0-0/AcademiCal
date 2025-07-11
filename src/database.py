import sqlite3

DB_name = 'assignments.db'

def DB_Connect():
    
    conn = sqlite3.connect(DB_name, isolation_level=None)
    
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT CHECK(status IN ('pending','completed')) DEFAULT 'pending')            
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    
def DB_Insert(title, description, due_data):
    conn = sqlite3.connect(DB_name)
    
    cur = conn.cursor()
    
    cur.execute('INSERT INTO assignments (title, description, due_date) VALUES (?, ?, ?)', (title, description, due_data))
    
    conn.commit()
    cur.close()
    conn.close()

def DB_Update(id, title, description, due_date, status):
    conn = sqlite3.connect(DB_name)    
    cur = conn.cursor()
    
    cur.execute('UPDATE assignments SET title = ?, description = ?, due_date = ?, status = ? WHERE id = ?', (title, description, due_date, status, id))    

    conn.commit()
    cur.close()
    conn.close()
    
def DB_Delete(id):
    conn = sqlite3.connect(DB_name)
    
    cur = conn.cursor()
    
    cur.execute('DELETE FROM assignments WHERE id = ?', (id,))
    
    conn.commit()
    cur.close()
    conn.close()

def DB_Check_All() -> list:
    conn = sqlite3.connect(DB_name)
    
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM assignments')
    
    row = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return row
