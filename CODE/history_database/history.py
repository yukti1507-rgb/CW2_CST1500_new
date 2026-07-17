import pandas as pd
import streamlit as st
import uuid
from history_database.db import get_connection, create_history_table

def save_history(processes, summary, identifier, algorithm):
        """
        Saves results of runs to history database

        The processes are stored along with the average values
        """
        conn = get_connection()
        #Creates the history table and ensure it exists
        create_history_table(conn)
        cur = conn.cursor()

        sql = 'INSERT INTO history (identifier, process_number, arrival_time, burst_time, waiting_time, turnaround_time, algorithm) VALUES (?, ?, ?, ?, ?, ?, ?)'
        #Sve each process in a different row
        for process in processes:    
            param = (identifier, process.process_number, process.arrival_time, process.burst_time, process.waiting_time, process.turnaround_time, algorithm)
            cur.execute(sql, param)

        #Stores the average values in a separate row
        avg_row = summary[-1]
        avg_wait = avg_row["Waiting Time"]
        avg_turn = avg_row["Turnaround Time"]

        avg_entry = (
            identifier,
            "Average",
            -1,
            -1,
            avg_wait,
            avg_turn,
            algorithm
        )

        cur.execute(sql, avg_entry)
        conn.commit()
        conn.close()
    
def export_as_csv(results):
    """
    Converts results table into a CSV file
    """
    df = pd.DataFrame(results)
    csv = df.to_csv(index=False)

    return csv

def initialise_save_session():
    """
    Ensures all required session states are initialised where necessary
    """

    defaults = {
        "save_confirmed": False,
        "save_history": False,
        "history_saved": False,
        "user_id": None,
        "username": None
    }

    #If not defined, the session states have the defined values
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def save_results_option(processes, summary, algorithm):
    """
    Displays the saving options such as anonymous ID and username to the user

    """
     
    initialise_save_session()

    #Ask user if they want ot save the run
    save_choice = st.radio("Would you like to save these results?", ["Yes", "No"])

    if save_choice == "Yes":

        #Provide user with different saving methods
        save_option = st.radio("How would you like to identify this history?", ["Anonymous ID", "My Name"])

        if save_option == "Anonymous ID":
            st.info("A temporary ID will be generated for this session. The saved history can be viewed on the history page using the ID.")
            if st.button("Confirm"):
                #Generate a unique ID for the session
                user_id = str(uuid.uuid4()).replace("-", "")[:8]
                st.session_state["user_id"] = user_id
                st.session_state["username"] = None
                st.session_state["save_confirmed"] = True
                st.session_state["save_history"] = True

                st.success(f"Your anonymous ID has been generated.")
                st.text_input("Copy this ID if you want to access these results later on the History page:", value=st.session_state["user_id"])

        elif save_option == "My Name":
            st.info("Your history will be saved with your chosen username. You can retrieve previous sessions on the History page using the username whenever you run the application again.")
            username = st.text_input("Enter your name")

            if st.button("Confirm username"):
                #Stores the username for later access through history page
                if username:
                    st.session_state["username"] = username
                    st.session_state["user_id"] = None
                    st.session_state["save_confirmed"] = True
                    st.session_state["save_history"] = True
                    
                    st.success("History will be saved using your username")
        
        #Ensures no duplicate entries are created when the page reruns
        if st.session_state["save_history"] and not st.session_state["history_saved"]:
            identifier = st.session_state["user_id"] if save_option == "Anonymous ID" else st.session_state["username"]
        
            save_history(processes, summary, identifier, algorithm)

    else:
        st.session_state["save_history"] = False
        st.info("The results will only be displayed during the current run.")
