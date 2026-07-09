import sqlite3

def get_connection():
        conn = sqlite3.connect('history_database/history.db', check_same_thread=False)
        return conn

    # CREATE TABLE
def create_history_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier TEXT,
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