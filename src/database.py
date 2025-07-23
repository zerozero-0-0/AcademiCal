import sqlite3
import os

DB_PATH = os.getenv('DATABASE_PATH', 'assignments.db')

def DB_Connect():
    
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    
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
    conn = sqlite3.connect(DB_PATH)
    
    cur = conn.cursor()
    
    cur.execute('INSERT INTO assignments (title, description, due_date) VALUES (?, ?, ?)', (title, description, due_data))
    
    conn.commit()
    cur.close()
    conn.close()

def DB_Update(id, title, description, due_date, status):
    conn = sqlite3.connect(DB_PATH)    
    cur = conn.cursor()
    
    cur.execute('UPDATE assignments SET title = ?, description = ?, due_date = ?, status = ? WHERE id = ?', (title, description, due_date, status, id))    

    conn.commit()
    cur.close()
    conn.close()
    
def DB_Delete(id):
    conn = sqlite3.connect(DB_PATH)
    
    cur = conn.cursor()
    
    cur.execute('DELETE FROM assignments WHERE id = ?', (id,))
    
    conn.commit()
    cur.close()
    conn.close()

def DB_Done(id: str) -> None:
    """
    課題をpendingからcompletedに変更する
    Args:
        id (str): 課題のID
    Returns:
        None
    """
    conn = sqlite3.connect(DB_PATH)
    
    cur = conn.cursor()
    
    cur.execute('UPDATE assignments SET status = "completed" WHERE id = ?', (id,))
    
    conn.commit()
    cur.close()
    conn.close()
    

def DB_Check_All() -> list:
    conn = sqlite3.connect(DB_PATH)
    
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM assignments')
    
    row = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return row

def DB_Check_Pending() -> list:
    """
    課題のうち、未完了のものを取得する
    Returns:
        list: 未完了の課題のリスト
    """
    conn = sqlite3.connect(DB_PATH)
    
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM assignments WHERE status = "pending"')
    
    row = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return row