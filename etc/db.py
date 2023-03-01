import sqlite3

from datetime import datetime

def create_table():
    conn = sqlite3.connect('etc/cocobongbong.db')
    cur = conn.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS session 
                    (name TEXT, president TEXT, id INTEGER, start Date DEFAULT NULL, end Date DEFAULT NULL, time INTEGER DEFAULT NULL, room TEXT DEFAULT NULL, maximum INTEGER DEFAULT NULL)''')
    cur.execute('CREATE TABLE IF NOT EXISTS student (id INTEGER, name TEXT, session TEXT)')

    conn.commit()
    conn.close()

def connect_table(table_name: str):
    conn = sqlite3.connect('etc/cocobongbong.db')
    cur = conn.cursor()

    return conn, cur

def add_session_in_db(session_name: str, president_name: str, president_id: int):
    conn, cur = connect_table('session')

    cur.execute('INSERT INTO session VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (session_name, president_name, president_id, None, None, None, None, None))

    conn.commit()
    conn.close()

def delete_session_from_db(session_name: str, president_id: int):
    conn, cur = connect_table('session')

    cur.execute('DELETE FROM session WHERE name = ? AND id = ?', (session_name, president_id))

    conn.commit()
    conn.close()

def add_student_in_db(student_id: int, student_name: str, session_name: str):
    conn, cur = connect_table('student')

    cur.execute('INSERT INTO student VALUES (?, ?, ?)', (student_id, student_name, session_name))

    conn.commit()
    conn.close()

def get_session_info():
    conn, cur = connect_table('session')

    cur.execute('SELECT * FROM session')
    session_info = cur.fetchall()

    conn.close()

    return session_info