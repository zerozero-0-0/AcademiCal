import sqlite3
from src.database.DB_name import DB_name

def DB_Insert(title, description, due_data):
    conn = sqlite3.connect(DB_name)

    cur = conn.cursor()

    cur.execute(
        "INSERT INTO assignments (title, description, due_date) VALUES (?, ?, ?)",
        (title, description, due_data),
    )

    conn.commit()
    cur.close()
    conn.close()


def DB_Update(id, title, description, due_date, status):
    conn = sqlite3.connect(DB_name)
    cur = conn.cursor()

    cur.execute(
        "UPDATE assignments SET title = ?, description = ?, due_date = ?, status = ? WHERE id = ?",
        (title, description, due_date, status, id),
    )

    conn.commit()
    cur.close()
    conn.close()


def DB_Delete(id):
    conn = sqlite3.connect(DB_name)

    cur = conn.cursor()

    cur.execute("DELETE FROM assignments WHERE id = ?", (id,))

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
    conn = sqlite3.connect(DB_name)

    cur = conn.cursor()

    cur.execute('UPDATE assignments SET status = "completed" WHERE id = ?', (id,))

    conn.commit()
    cur.close()
    conn.close()


def DB_Check_All() -> list:
    conn = sqlite3.connect(DB_name)

    cur = conn.cursor()

    cur.execute("SELECT * FROM assignments")

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
    conn = sqlite3.connect(DB_name)

    cur = conn.cursor()

    cur.execute('SELECT * FROM assignments WHERE status = "pending"')

    row = cur.fetchall()

    cur.close()
    conn.close()

    return row
