import streamlit as st
import pandas as pd
from logic.scheduler_logic import Process
from logic.SJF_logic import SJF_Scheduler
from history_database.history import save_results_option, export_as_csv

st.set_page_config(page_title= "Shortest Job First", page_icon= "⚡", layout="wide")
st.title("CPU Algorithm - Shortest Job First")

st.image("SJF banner2.jpeg", width=1200)

#Ensures processes have been created on the home page
if "processes" not in st.session_state:
    st.warning("No processes found. Please go back to the main page and input the processes.")
    st.stop()

processes = st.session_state['processes']

#Allows the uer to skip animation
skip_animation = st.checkbox("Skip execution animation")

if st.button("Run SJF"):
    #Reset session states for new execution
    st.session_state["history_saved"] = False
    st.session_state["save_history"] = False
    st.session_state["skip_animation"] = skip_animation
        
    #Create scheduler and add processes to the list
    scheduler = SJF_Scheduler()

    for p in processes:
        process = Process(p["Process Number"], p["Arrival Time"], p["Burst Time"])
        scheduler.add_process(process)

    #Run the algorithm and store the results
    results = scheduler.run()
    summary = scheduler.get_summary_table()

    #Store results across reruns
    st.session_state["sjf_results"] = results
    st.session_state["sjf_summary"] = summary

if "sjf_results" in st.session_state:
    #Display summary table
    summary_table = pd.DataFrame(st.session_state["sjf_summary"])
    st.table(summary_table)

    algorithm_name = "SJF"

    #Allow the user to save results of the run to a database
    save_results_option(st.session_state["sjf_results"], st.session_state["sjf_summary"], algorithm_name)

    #Allow user to download a csv file of the results
    download_csv = st.radio("Would you like to download the results as a csv file?", ["Yes", "No"])
    if download_csv == "Yes":
        csv = export_as_csv(st.session_state["sjf_summary"])
        st.download_button(label="Download", data=csv, file_name="SJF_results.csv", mime="text/csv")
