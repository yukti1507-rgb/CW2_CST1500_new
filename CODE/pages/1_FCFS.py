import streamlit as st
from logic.FCFS_logic import Process, Scheduler
import pandas as pd

st.title("CPU Algorithm - First Come, First Served")

if "processes" not in st.session_state:
    st.warning("No processes found. Please go back to the main page and input the processes.")
    st.stop()

processes = st.session_state['processes']

scheduler = Scheduler()

for process_number, burst_time, arrival_time in processes:
    process  = Process(process_number, burst_time, arrival_time)
    scheduler.add_process(process)

scheduler.run()
    
average_waiting_time = scheduler.calculate_average_waiting_time()
average_turnaround_time = scheduler.calculate_average_turnaround_time()

st.write(f"**Average Waiting Time:** {average_waiting_time:.2f}")
st.write(f"**Average Turnaround Time:** {average_turnaround_time:.2f}")








# import csvs, export as csvs
# gaant charts proportionate
# propose best algorithms based on turnaround time and waiting time

    