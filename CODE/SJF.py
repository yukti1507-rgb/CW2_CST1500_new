# app.py
import streamlit as st
import pandas as pd
import altair as alt
import time
from OOP import ProcessThread, SJFScheduler  

# Streamlit user interface
st.set_page_config(page_title="SJF", layout="wide")
st.title("CPU Algorithm - Shortest Job First")

st.badge("Enter number of processes:", color="blue")
num_processes = st.number_input("", min_value=3, step=1)
processes = []

for i in range(int(num_processes)):
    col1, col2 = st.columns(2)
    with col1:
        st.badge(f"Enter burst time for process {i+1}", color="grey")
        burst_time = st.number_input("", min_value=1, step=1, key=f"burst_{i}")
    with col2:
        st.badge(f"Enter arrival time for process {i+1}", color="grey")
        arrival_time = st.number_input("", min_value=0, step=1, key=f"arrival_{i}")
    processes.append(ProcessThread(i+1, arrival_time, burst_time))

if st.button("Run SJF"):
    table_placeholder = st.empty()
    scheduler = SJFScheduler(processes)

    
    results, timeline = scheduler.run(table_placeholder, st, time, pd)

    st.badge("All processes have been completed")

    average_waiting_time = sum(p.waiting_time for p in results) / num_processes
    average_turnaround_time = sum(p.turnaround_time for p in results) / num_processes

    st.write(f"**Average Waiting Time:** {average_waiting_time:.2f}")
    st.write(f"**Average Turnaround Time:** {average_turnaround_time:.2f}")

    # Gantt chart 
    gantt_data = pd.DataFrame(timeline)
    chart = alt.Chart(gantt_data).mark_bar(color="darkgrey").encode(
        x="Start",
        x2="Finish",
        y=alt.Y("Process", sort=None)
).properties(title="Gantt Chart", width=600, height=300)


    st.altair_chart(chart, use_container_width=True)
