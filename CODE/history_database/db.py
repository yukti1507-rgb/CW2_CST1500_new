import sqlite3
import pandas as pd

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

def get_specific_identifier(identifier):
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM history WHERE identifier = ? ORDER BY timestamp DESC",
        conn,
        params=(identifier,)
    )
    conn.close()
    return df

def get_specific_algorithm(identifier, algorithm):
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM history WHERE identifier = ? AND algorithm = ? ORDER BY timestamp DESC",
        conn,
        params=(identifier, algorithm)
    )
    conn.close()
    return df

def get_specific_timestamp(identifier, timestamp):
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM history WHERE identifier = ? AND timestamp = ?",
        conn,
        params=(identifier, timestamp)
    )
    conn.close()
    return df

def delete_run(identifier, timestamp):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM history WHERE identifier = ? AND timestamp = ?",
        (identifier, timestamp)
    )
    conn.commit()
    conn.close()
