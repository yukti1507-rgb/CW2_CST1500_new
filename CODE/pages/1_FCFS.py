import streamlit as st
import uuid
from logic import Process, FCFS_Scheduler
from history_database.history import save_history, export_as_csv

st.title("CPU Algorithm - First Come, First Served")

if "processes" not in st.session_state:
    st.warning("No processes found. Please go back to the main page and input the processes.")
    st.stop()

processes = st.session_state['processes']

scheduler = FCFS_Scheduler()

for p in processes:
    process  = Process(p["Process Number"], p["Arrival Time"], p["Burst Time"])
    scheduler.add_process(process)

scheduler.run()

if "save_confirmed" not in st.session_state:
    st.session_state["save_confirmed"] = False

if "save_history" not in st.session_state:
    st.session_state["save_history"] = False

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

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
    
        save_history(scheduler.processes, identifier, "FCFS")

if save_choice == "No":
    st.session_state["save_history"] = False
    st.info("The results will only be displayed during the current run.")


download_csv = st.radio("Would you like to download the results as a csv file?", ["Yes", "No"])

if download_csv == "Yes":
    csv = export_as_csv(scheduler.results)
    st.download_button(label="Download", data=csv, file_name="FCFS_results.csv", mime="text/csv")
