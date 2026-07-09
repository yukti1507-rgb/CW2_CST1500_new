import time
import random
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

#Defining the thread class 
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
    
    def add_process(self, process):
        self.processes.append(process)
    
    def calculate_average_waiting_time(self):
        total_waiting_time = sum(process.waiting_time for process in self.processes)
        return total_waiting_time / len(self.processes) if self.processes else 0
    
    def calculate_average_turnaround_time(self):
        total_turnaround_time = sum(process.turnaround_time for process in self.processes)
        return total_turnaround_time / len(self.processes) if self.processes else 0
    
    def progress_of_process(self, process):
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text(f"Running process {process.process_number}...")
        animation_time = (process.burst_time * 0.2)
        for percent in range(0, 101, 20):
            progress_bar.progress(percent)
            time.sleep(animation_time / 10)
        st.success(f"Process {process.process_number} has been completed in {process.burst_time} second(s).\n")

    def display_gantt_chart(self):
        fig = go.Figure()

        colors = [
            "blue",
            "orange",
            "green",
            "red",
            "purple"
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
            use_container_width=True,
            key="fcfs_gantt"
        )


    def display_results(self):
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
    
    
class FCFS_Scheduler(Scheduler):
    def __init__(self):
        super().__init__()
    
    def run(self):
        self.processes.sort(key=lambda x: x.arrival_time)

        if not self.processes:
            return

        current_time = 0
        
        for process in self.processes:
            if current_time < process.arrival_time:
                self.timeline.append({
                    "Process": "Idle",
                    "Start": current_time,
                    "Finish": process.arrival_time
                })
                current_time = process.arrival_time

            process.start_time = current_time
            process.waiting_time = process.start_time - process.arrival_time
            process.turnaround_time = (process.waiting_time + process.burst_time)
            current_time += process.burst_time
            process.finish_time = current_time


            self.timeline.append({
            "Process": process.process_number,
            "Start": process.start_time,
            "Finish": process.finish_time
            })
        

       
        self.display_results()



class SJF_Scheduler(Scheduler):
    def __init__(self):
        super().__init__()
   
    def run(self):
        ready_queue = self.processes.copy()
        self.current_time = 0

        while ready_queue:
            # Find all processes that have arrived
            available = [p for p in ready_queue if p.arrival_time <= self.current_time]

            # If none have arrived yet, jump to next arrival
            if not available:
                next_arrival = min(p.arrival_time for p in ready_queue)

                # CPU idle until next arrival
                self.timeline.append({
                    "Process": "Idle",
                    "Start": self.current_time,
                    "Finish": next_arrival
                })

                self.current_time = next_arrival
                available = [p for p in ready_queue if p.arrival_time <= self.current_time]

            # Pick shortest burst among available
            available.sort(key=lambda p: p.burst_time)
            process = available[0]
            ready_queue.remove(process)

            # Start time
            process.start_time = self.current_time

            # Waiting time
            process.waiting_time = process.start_time - process.arrival_time

            # Run the process
            self.current_time += process.burst_time

            # Finish time
            process.finish_time = self.current_time

            # Turnaround time
            process.turnaround_time = process.finish_time - process.arrival_time

            # Add to timeline
            self.timeline.append({
                "Process": process.process_number,
                "Start": process.start_time,
                "Finish": process.finish_time
            })

        self.display_results()


         

# ROUND ROBIN

class RR_Scheduler(Scheduler):
    def __init__(self, time_quantum):
        super().__init__()
        self.time_quantum = time_quantum

    def run(self):
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        ready_queue = []
        self.current_time = 0

        while processes or ready_queue:

            # Add newly arrived processes
            while processes and processes[0].arrival_time <= self.current_time:
                ready_queue.append(processes.pop(0))

            # CPU idle if no process is ready
            if not ready_queue:
                next_arrival = processes[0].arrival_time

                # Add idle block
                self.timeline.append({
                    "Process": "Idle",
                    "Start": self.current_time,
                    "Finish": next_arrival
                })

                self.current_time = next_arrival
                continue

            # Pop next process from queue
            process = ready_queue.pop(0)
            start_time = self.current_time

            # Run for quantum or remaining burst
            run_time = min(self.time_quantum, process.remaining_time)
            process.remaining_time -= run_time
            self.current_time += run_time

            # Add execution block
            self.timeline.append({
                "Process": process.process_number,
                "Start": start_time,
                "Finish": self.current_time
            })

            # Add newly arrived processes during execution
            while processes and processes[0].arrival_time <= self.current_time:
                ready_queue.append(processes.pop(0))

            # Requeue if not finished
            if process.remaining_time > 0:
                ready_queue.append(process)
            else:
                process.finish_time = self.current_time
                process.turnaround_time = process.finish_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time

        self.display_results()


    
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