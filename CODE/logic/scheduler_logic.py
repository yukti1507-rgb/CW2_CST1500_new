import time
import random
import threading
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

class Process():
    def __init__(self, process_number, arrival_time, burst_time):
        super().__init__()
        self.process_number = process_number
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        self.remaining_time = burst_time
        self.start_time = 0
        self.finish_time = 0

class Scheduler:
    def __init__(self):
        self.processes = []
        self.current_time = 0
        self.results = []
        self.timeline =[] 
        self.table_placeholder = st.empty()
        self.silent = False
        self.cpu_lock = threading.Lock()
    
    
    def add_process(self, process):
        self.processes.append(process)
    
    def calculate_average_waiting_time(self):
        total_waiting_time = sum(process.waiting_time for process in self.processes)
        return total_waiting_time / len(self.processes) if self.processes else 0
    
    def calculate_average_turnaround_time(self):
        total_turnaround_time = sum(process.turnaround_time for process in self.processes)
        return total_turnaround_time / len(self.processes) if self.processes else 0
    
    def get_summary(self):
        return {
            "Average Waiting Time": self.calculate_average_waiting_time(),
            "Average Turnaround Time": self.calculate_average_turnaround_time()
        }

    def progress_of_process(self, process):
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text(f"Running process {process.process_number}...")
        animation_time = (process.burst_time * 0.2)
        for percent in range(0, 101, 20):
            progress_bar.progress(percent)
            time.sleep(animation_time / 10)
        st.info(f"Process {process.process_number} has been completed in {process.burst_time} second(s).\n")

    def display_gantt_chart(self):
        fig = go.Figure()

        colors = [
            "light blue",
            "violet",
            "purple",
            "pink",
            "gray"
        ]

        for i, block in enumerate(self.timeline):

            duration = block["Finish"] - block["Start"]

            if block["Process"] == "Idle":
                color = "lightgray"
                label = "Idle"
            else:
                color = colors[i % len(colors)]
                label = f"P{block['Process']}"

            fig.add_trace(
                go.Bar(
                    x=[duration],
                    y=["CPU"],                 # SAME ROW
                    base=[block["Start"]],     # START POSITION
                    orientation="h",
                    text=label,
                    textposition="inside",
                    marker=dict(color=color),
                    hovertemplate=(
                        f"{label}<br>"
                        f"Start: {block['Start']}<br>"
                        f"Finish: {block['Finish']}<br>"
                        f"Duration: {duration}"
                        "<extra></extra>"
                    )
                )
            )
        
        time_points = []

        for block in self.timeline:
            time_points.append(block["Start"])
            time_points.append(block["Finish"])

        time_points = sorted(set(time_points))

        fig.update_layout(
            barmode="stack",
            title="CPU Scheduling Gantt Chart",
            xaxis_title="Time",
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                showticklabels=False
            ),
            height=300,
            showlegend=False
        )

        fig.update_xaxes(
            tickmode="array",
            tickvals=time_points,
            ticktext=[str(t) for t in time_points],
            title="CPU Time"
        )

        fig.update_traces(
            width=0.5,
            textposition="inside",
            insidetextanchor="middle"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    def display_results(self):
        if self.silent:
            return
        
        for process in self.processes:
            self.progress_of_process(process)
            
            self.results.append({
            "Process Number": process.process_number,
            "Arrival Time": process.arrival_time,
            "Burst Time": process.burst_time,
            "Waiting Time": process.waiting_time,
            "Turnaround Time": process.turnaround_time
            })

            df = pd.DataFrame(self.results)
            self.table_placeholder.dataframe(df)
        self.display_gantt_chart()

class ProcessThread(threading.Thread):
    def __init__(self, process, run_time, cpu_lock):
        super().__init__()
        self.process = process
        self.run_time = run_time
        self.cpu_lock = cpu_lock

    def run(self):
        with self.cpu_lock:
            time.sleep(self.run_time)
 
class RandomGenerator:
    def generate_random_processes(num_processes, max_arrival=20, max_burst=20):
        processes = []
        for i in range(num_processes):
            processes.append({
                "Process Number": (i+1),
                "Arrival Time": random.randint(0, max_arrival),
                "Burst Time": random.randint(1, max_burst)
            })  
        return processes