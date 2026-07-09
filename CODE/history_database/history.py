import pandas as pd
import streamlit as st
import uuid
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

def initialise_save_session():

    defaults = {
        "save_confirmed": False,
        "save_history": False,
        "user_id": None,
        "username": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def save_results_option(scheduler, algorithm):
     
    initialise_save_session()

    save_choice = st.radio("Would you like to save these results?", ["Yes", "No"])


    if save_choice == "Yes":

        save_option = st.radio("How would you like to identify this history?", ["Anonymous ID", "My Name"])

        if save_option == "Anonymous ID":
            st.info("A temporary ID will be generated. The saved history can be viewed while this session remains active.")
            st.warning("If you leave or restart the application, your anonymous history may no longer be accessible.")
            if st.button("Confirm"):
                user_id = str(uuid.uuid4()).replace("-", "")[:8]
                st.session_state["user_id"] = user_id
                st.session_state["username"] = None
                st.session_state["save_confirmed"] = True
                st.session_state["save_history"] = True

                st.success(f"Your anonymous ID has been generated.")
                st.text_input("Copy this ID if you want to access these results later on the History page:", value=st.session_state["user_id"])

            
        elif save_option == "My Name":
            st.info("Your history will be saved with your chosen username. You can retrieve previous sessions on the History page using the username whenever youi run the application again.")
            username = st.text_input("Enter your name")

            if st.button ("Confirm username"):
                if username:
                    st.session_state["username"] = username
                    st.session_state["user_id"] = None
                    st.session_state["save_confirmed"] = True
                    st.session_state["save_history"] = True
                    
                    st.success("History will be saved using your username")
        
        if st.session_state["save_history"]:
            if save_option == "Anonymous ID":
                identifier = st.session_state["user_id"]
            else:
                identifier = st.session_state["username"]
        
            save_history(scheduler.processes, identifier, algorithm)

    else:
        st.session_state["save_history"] = False
        st.info("The results will only be displayed during the current run.")


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
