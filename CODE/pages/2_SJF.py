import streamlit as st
import pandas as pd
from logic.scheduler_logic import Process
from logic.SJF_logic import SJF_Scheduler
from history_database.history import save_results_option, export_as_csv
import streamlit as st
from logic import Process, SJF_Scheduler
from history_database.history import save_results_option, export_as_csv

st.set_page_config(page_title= "Shortest Job First", page_icon= "⚡", layout="wide")
st.title("CPU Algorithm - Shortest Job First")

if "processes" not in st.session_state:
    st.warning("No processes found. Please go back to the main page and input the processes.")
    st.stop()

processes = st.session_state['processes']


if st.button("Run SJF"):
    scheduler = SJF_Scheduler()
    for p in processes:
        process = Process(p["Process Number"], p["Arrival Time"], p["Burst Time"])
        scheduler.add_process(process)

    results, summary = scheduler.run()

    st.session_state["sjf_results"] = results
    st.session_state["sjf_summary"] = summary
    st.session_state["sjf_csv"] = scheduler.results

if "sjf_results" in st.session_state:
    summary_table = pd.DataFrame([st.session_state["sjf_summary"]])
    st.table(summary_table)

    algorithm_name = "SJF"

    save_results_option(st.session_state["sjf_results"], st.session_state["sjf_summary"], algorithm_name)

    download_csv = st.radio("Would you like to download the results as a csv file?", ["Yes", "No"])
    if download_csv == "Yes":
        csv = export_as_csv(st.session_state["sjf_csv"])
        st.download_button(label="Download", data=csv, file_name="SJF_results.csv", mime="text/csv")
