import sqlite3

from datetime import datetime

def create_table():
    conn = sqlite3.connect('etc/cocobongbong.db')
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS president (id INTEGER, name TEXT, session TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS student (id INTEGER, name TEXT, session TEXT)')

    conn.commit()
    conn.close()

def connect_table(table_name: str):
    conn = sqlite3.connect('etc/cocobongbong.db')
    cur = conn.cursor()

    return conn, cur

def add_president_in_db(president_id: int, president_name: str, session_name: str):
    conn, cur = connect_table('president')

    cur.execute('INSERT INTO president VALUES (?, ?, ?)', (president_id, president_name, session_name))

    conn.commit()
    conn.close()

def delete_president_from_db(president_id: int, session_name: str):
    conn, cur = connect_table('president')

    cur.execute('DELETE FROM president WHERE id = ? AND session = ?', (president_id, session_name))

    conn.commit()
    conn.close()

def add_student_in_db(student_id: int, student_name: str, session_name: str):
    conn, cur = connect_table('student')

    cur.execute('INSERT INTO student VALUES (?, ?, ?)', (student_id, student_name, session_name))

    conn.commit()
    conn.close()