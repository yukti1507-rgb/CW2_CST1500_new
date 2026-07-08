import sqlite3

def get_connection():
    conn = sqlite3.connect('CODE/history_database/history.db', check_same_thread=False)
    return conn

# CREATE TABLE
def create_history_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        process_number INTEGER NOT NULL,
        arrival_time INTEGER NOT NULL,
        burst_time INTEGER NOT NULL,
        waiting_time INTEGER NOT NULL,
        turnaround_time INTEGER NOT NULL,
        algorithm TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );'''
    cur.execute(sql)
    conn.commit()

# INSERT (parameterized — prevents SQL injection)
def save_history(conn, process):
    cur = conn.cursor()
    sql = 'INSERT INTO history (process_number, arrival_time, burst_time, waiting_time, turnaround_time, algorithm) VALUES (?, ?, ?, ?, ?, ?)'
    param = (process.process_number, process.arrival_time, process.burst_time, process.waiting_time, process.turnaround_time, process.algorithm)
    cur.execute(sql, param) 
    conn.commit()

