import streamlit as st
from logic import Process, RR_Scheduler
from history_database.history import save_results_option, export_as_csv


st.set_page_config(page_title= "Round Robin", page_icon= "🔄", layout="wide")
st.title("CPU Algorithm - Round Robin")

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


if st.button("Run RR"):
    scheduler = RR_Scheduler(time_quantum=time_quantum)

    for p in processes:
        process = Process(p["Process Number"], p["Arrival Time"], p["Burst Time"])
        scheduler.add_process(process)

    scheduler.run()

    algorithm_name = "RR"
    save_results_option(scheduler, algorithm_name)

    download_csv = st.radio("Would you like to download the results as a csv file?", ["Yes", "No"])
    if download_csv == "Yes":
        csv = export_as_csv(scheduler.results)
        st.download_button(label="Download", data=csv, file_name="RR_results.csv", mime="text/csv")
