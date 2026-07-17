import streamlit as st
import pandas as pd
from logic.scheduler_logic import RandomGenerator

st.set_page_config(page_title="CPU Scheduling Algorithms", page_icon= "🏡", layout= "wide")

st.title("Welcome to CPU Scheduling Algorithms!")

def choose_algorithm(processes):
    fcfs, sjf, rr = st.columns(3)

    run_fcfs = fcfs.button("Go to FCFS Page")
    if run_fcfs:
        st.session_state['processes'] = processes
        st.switch_page("pages/1_FCFS.py")
    
    run_sjf = sjf.button("Go to SJF Page")
    if run_sjf:
        st.session_state['processes'] = processes
        st.switch_page("pages/2_SJF.py")
    
    run_rr = rr.button("Go to RR Page")
    if run_rr:
        st.session_state['processes'] = processes
        st.switch_page("pages/3_RR.py")

num_processes = st.slider("Number of processes", min_value=1, max_value=50,value=3)      
input_method = st.selectbox("Select input method:",["Input values manually", "Generate random values", "Import CSV file"])

if input_method == "Input values manually":
    processes =[]

    col1, col2 = st.columns(2)
    col1.subheader("Arrival Time")
    col2.subheader("Burst Time")
#Prompting user to input burst times for each process
    for i in range(int(num_processes)):
        col1.badge(f"Enter arrival time for process {i+1}",color="violet")
        arrival_time= col1.number_input(f"", min_value=0, step=1, key=f"arrival_{i}")

        col2.badge(f"Enter burst time for process {i+1}",color="blue")
        burst_time= col2.number_input(f"", min_value=1, step=1, key=f"burst_{i}")
        
        processes.append({
            "Process Number" : i+1,
            "Arrival Time" : arrival_time,
            "Burst Time" : burst_time})
    
    choose_algorithm(processes)

elif input_method == "Generate random values":
    if st.button("Generate"):
        processes = RandomGenerator.generate_random_processes(num_processes)
        st.session_state['processes'] = processes   # <-- persist here
        df = pd.DataFrame(processes)
        st.dataframe(df)

        
    if "processes" in st.session_state:
        choose_algorithm(st.session_state["processes"])

#   MIGHT PUT IT SOMEWHERE ELSE
elif input_method == "Import CSV file":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("CSV file uploaded successfully!")
        st.dataframe(df)

        processes = df.to_dict(orient="records")
        st.session_state['processes'] = processes   # <-- persist here
        choose_algorithm(st.session_state["processes"])
