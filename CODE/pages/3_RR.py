import streamlit as st
import pandas as pd
from logic.scheduler_logic import Process
from logic.RR_logic import RR_Scheduler
from history_database.history import save_results_option, export_as_csv

st.set_page_config(page_title= "Round Robin", page_icon= "🔄", layout="wide")
st.title("CPU Algorithm - Round Robin")


st.image("RR banner.jpeg", width=1200)

if "processes" not in st.session_state:
    st.warning("No processes found. Please go back to the main page and input the processes.")
    st.stop()

processes = st.session_state['processes']

# Time quantum input (default = 2)
st.badge("Enter Time Quantum (Recommended: 2)", color="blue")
time_quantum = st.number_input(
    "",
    min_value=1,
    step=1,
    value=2
)

skip_animation = st.checkbox("Skip execution animation")

if st.button("Run RR"):
    st.session_state["skip_animation"] = skip_animation

    if "skip_animation" not in st.session_state:
        st.session_state["skip_animation"] = False
        
    scheduler = RR_Scheduler(time_quantum=time_quantum)

    for p in processes:
        process = Process(p["Process Number"], p["Arrival Time"], p["Burst Time"])
        scheduler.add_process(process)

    results = scheduler.run()
    summary = scheduler.get_summary_table()

    st.session_state["rr_results"] = results
    st.session_state["rr_summary"] = summary

if "rr_results" in st.session_state:
    summary_table = pd.DataFrame(st.session_state["rr_summary"])
    st.table(summary_table)

    algorithm_name = "RR"

    save_results_option(st.session_state["rr_results"], st.session_state["rr_summary"], algorithm_name)

    download_csv = st.radio("Would you like to download the results as a csv file?", ["Yes", "No"])
    if download_csv == "Yes":
        csv = export_as_csv(st.session_state["rr_summary"])
        st.download_button(label="Download", data=csv, file_name="RR_results.csv", mime="text/csv")
