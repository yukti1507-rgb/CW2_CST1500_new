import streamlit as st
import pandas as pd
from logic.scheduler_logic import Process
from logic.FCFS_logic import FCFS_Scheduler
from history_database.history import save_results_option, export_as_csv

st.set_page_config(page_title= "First Come, First Served", page_icon= "🕰️", layout="wide")
st.title("CPU Algorithm - First Come, First Served")

st.image("FCFS banner.jpeg", width=1200)

#Ensures processes have been created on the home page
if "processes" not in st.session_state:
    st.warning("No processes found. Please go back to the main page and input the processes.")
    st.stop()

processes = st.session_state['processes']

#Allows the uer to skip animation
skip_animation = st.checkbox("Skip execution animation")

if st.button("Run FCFS"):
    #Reset session states for new execution
    st.session_state["history_saved"] = False
    st.session_state["save_history"] = False
    st.session_state["skip_animation"] = skip_animation
        
    #Create scheduler and add processes to the list
    scheduler = FCFS_Scheduler()

    for p in processes:
        process = Process(p["Process Number"], p["Arrival Time"], p["Burst Time"])
        scheduler.add_process(process)

    #Run the algorithm and store the results
    results = scheduler.run()
    summary = scheduler.get_summary_table()

    #Store results across reruns
    st.session_state["fcfs_results"] = results
    st.session_state["fcfs_summary"] = summary

if "fcfs_results" in st.session_state:
    #Display summary table
    summary_table = pd.DataFrame(st.session_state["fcfs_summary"])
    st.table(summary_table)

    algorithm_name = "FCFS"

    #Allow the user to save results of the run to a database
    save_results_option(st.session_state["fcfs_results"], st.session_state["fcfs_summary"], algorithm_name)

    #Allow user to download a csv file of the results
    download_csv = st.radio("Would you like to download the results as a csv file?", ["Yes", "No"])
    if download_csv == "Yes":
        csv = export_as_csv(st.session_state["fcfs_summary"])
        st.download_button(label="Download", data=csv, file_name="FCFS_results.csv", mime="text/csv")
