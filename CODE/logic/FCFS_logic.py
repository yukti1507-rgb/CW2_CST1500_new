import streamlit as st
import pandas as pd
import plotly as px
import time
import random

from history_database.db import get_connection, save_history

class Process:
    def __init__(self, process_number, burst_time, arrival_time):
        self.process_number = process_number
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.start_time = 0
        self.finish_time = 0
    
       

class Scheduler:
    def __init__(self):
        self.processes = []
        self.table_placeholder = st.empty()
        self.results = []
    
    def add_process(self, process):
        self.processes.append(process)
    
    def calculate_waiting_time(self):
        if not self.processes:
            return
        
        self.processes.sort(key=lambda x: x.arrival_time)

        current_time = 0
        
        for process in self.processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            process.start_time = current_time
            process.waiting_time = process.start_time - process.arrival_time
            current_time += process.burst_time
            process.finish_time = current_time


    
    def calculating_turnaround_time(self):
        for process in self.processes:
            process.turnaround_time = (process.waiting_time + process.burst_time)
    
    def calculate_average_waiting_time(self):
        total_waiting_time = sum(process.waiting_time for process in self.processes)
        return total_waiting_time / len(self.processes) if self.processes else 0
    
    def calculate_average_turnaround_time(self):
        total_turnaround_time = sum(process.turnaround_time for process in self.processes)
        return total_turnaround_time / len(self.processes) if self.processes else 0
    
    def animate_processes(self, process):
            status = st.empty()
            progress = st.empty()

            status.info(f"Process {process.process_number} is running...")
            progress_bar = progress.progress(0)
            animation_time = (process.burst_time * 0.2)

            for i in range(100):
                time.sleep(animation_time / 100)
                progress_bar.progress(i + 1)

            status.success(f"Process {process.process_number} has been completed in {process.burst_time} seconds.")
            progress.empty()

    def display_gaant_chart(self):
        gaant_data = []

        for process in self.processes:
            gaant_data.append({
                "Process": f"P{process.process_number}",
                "Start": process.start_time,
                "Finish": process.finish_time
            })
        
        

    def run_processes(self):
        for process in self.processes:
            self.animate_processes(process)
            
            self.results.append({
            "Process Number": process.process_number,
            "Arrival Time": process.arrival_time,
            "Burst Time": process.burst_time,
            "Waiting Time": process.waiting_time,
            "Turnaround Time": process.turnaround_time
            })

            conn = get_connection()  # Assuming you have a function to get the database connection

            save_history(conn, process, algorithm="FCFS")

            conn.close()

            self.table_placeholder.dataframe(pd.DataFrame(self.results))
    
    def run(self):
        self.calculate_waiting_time()
        self.calculating_turnaround_time()
        self.run_processes()
        

class RandomGenerator:
    def generate_random_processes(num_processes, max_arrival=20, max_burst=20):
        processes = []
        for i in range(num_processes):
            processes.append({
                "Process Number": i +1,
                "Arrival time": random.randint(0, max_arrival),
                "Burst time": random.randint(1, max_burst)
            })  
        return processes



def recommended_algorithm():
    recommended = st.expander("Recommended Algorithm")
    recommended.write(f"Based on the input values, the recommended algorithm is: {recommended_algorithm}.")

   
        

