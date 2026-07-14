import streamlit as st
import pandas as pd
from logic.scheduler_logic import Process
from logic.FCFS_logic import FCFS_Scheduler
from history_database.history import save_results_option, export_as_csv

st.set_page_config(page_title= "First Come, First Served", page_icon= "🕰️", layout="wide")
st.title("CPU Algorithm - First Come, First Served")

if "processes" not in st.session_state:
    st.warning("No processes found. Please go back to the main page and input the processes.")
    st.stop()

processes = st.session_state['processes']


if st.button("Run FCFS"):
    scheduler = FCFS_Scheduler()

    for p in processes:
        process = Process(p["Process Number"], p["Arrival Time"], p["Burst Time"])
        scheduler.add_process(process)

results, summary = scheduler.run()

summary_table = pd.DataFrame([summary])
st.table(summary_table)

algorithm_name = "FCFS"

save_results_option(results, summary, algorithm_name)

    download_csv = st.radio("Would you like to download the results as a csv file?", ["Yes", "No"])
    if download_csv == "Yes":
        csv = export_as_csv(scheduler.results)
        st.download_button(label="Download", data=csv, file_name="FCFS_results.csv", mime="text/csv")
