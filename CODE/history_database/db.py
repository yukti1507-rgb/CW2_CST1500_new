import sqlite3
import pandas as pd

def get_connection():
        """
        Creates a connection to the database
        """
        # check same thread ensures connection is shared properly among threads
        conn = sqlite3.connect('history_database/history.db', check_same_thread=False)
        return conn

    # CREATE TABLE
def create_history_table(conn):
    """
    Creates history table if it does not exist
    """
    cur = conn.cursor()

    #Stores algorithm name and timestamp for easy retrieval
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


def get_specific_algorithm(identifier, algorithm):
    """
    Retrieves runs according to algorithm name and identifier
    """
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM history WHERE identifier = ? AND algorithm = ? ORDER BY timestamp DESC",
        conn,
        params=(identifier, algorithm)
    )
    conn.close()
    return df

def get_specific_timestamp(identifier, timestamp):
    """
    Retrieves runs according to timestamp and identifier
    """
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM history WHERE identifier = ? AND timestamp = ?",
        conn,
        params=(identifier, timestamp)
    )
    conn.close()
    return df

def delete_run(identifier, timestamp):
    """
    Deletes a run from the database based on timestamp
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM history WHERE identifier = ? AND timestamp = ?",
        (identifier, timestamp)
    )
    conn.commit()
    conn.close()
