import pandas as pd
from history_database.db import get_connection, create_history_table

def save_history(processes, identifier, algorithm):
        conn = get_connection()
        create_history_table(conn)
        cur = conn.cursor()
        sql = 'INSERT INTO history (identifier, process_number, arrival_time, burst_time, waiting_time, turnaround_time, algorithm) VALUES (?, ?, ?, ?, ?, ?, ?)'
        for process in processes:    
            param = (identifier, process.process_number, process.arrival_time, process.burst_time, process.waiting_time, process.turnaround_time, algorithm)
            cur.execute(sql, param) 
        conn.commit()
        conn.close()
    
def export_as_csv(results):
    df = pd.DataFrame(results)
    csv = df.to_csv(index=False)

    return csv