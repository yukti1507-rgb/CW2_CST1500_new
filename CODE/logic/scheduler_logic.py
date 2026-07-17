import time
import random
import threading
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

class Process:
    """
    Represents a process in the CPU scheduling.

    It assigns values to object properties such as arrival time, burst time and all the calculated values.
    """
    def __init__(self, process_number, arrival_time, burst_time):
        super().__init__()

        #Unique number for the process
        self.process_number = process_number

        #Time at which the process enters the queue
        self.arrival_time = arrival_time

        #Total CPU time used by the process
        self.burst_time = burst_time

        #Total time the process waits iin the queue before execution 
        self.waiting_time = 0

        #Total time from arrival time to finish time
        self.turnaround_time = 0

        #Time left for execution in Round Robin
        self.remaining_time = burst_time

        #Stores when the process starts and finishes to help build timeline
        self.start_time = 0
        self.finish_time = 0

class Scheduler:
    """
    Scheduler class containing shared methods by all CPU scheduling algorithms

    It performs execution of process and calculations, animation and display of results 
    """
    def __init__(self):
        #List for all processes in the scheduler
        self.processes = []

        #Keeps track of current CPU time
        self.current_time = 0

        #List containing results of processes for display
        self.results = []

        #List containing timeline used for gantt chart
        self.timeline =[] 

        #List containing order in which processes are executed after sorting
        self.execution_order = []

        #List containing time for execution of time slices in Round Robin
        self.execution_time = []

        #List containing boolean values for completion of Round Robin
        self.execution_completed = []

        #Placeholder for live update of table
        self.table_placeholder = st.empty()

        #Runs processes without display of results for history page
        self.silent = False

        #Lock preventing multiple processes from accessing CPU simultaneously in Round Robin
        self.cpu_lock = threading.Lock()
    
    
    def add_process(self, process):
        """
        Adds process to scheduler list of processes
        """
        self.processes.append(process)
    
    def calculate_average_waiting_time(self):
        """
        Calculates average waiting time for all processes
        """
        total_waiting_time = sum(process.waiting_time for process in self.processes)
        return total_waiting_time / len(self.processes) if self.processes else 0
    
    def calculate_average_turnaround_time(self):
        """
        Calculates average turnaround time for all processes
        """
        total_turnaround_time = sum(process.turnaround_time for process in self.processes)
        return total_turnaround_time / len(self.processes) if self.processes else 0


    def progress_of_process(self, process,run_time=None, completed=False):
        """
        Dispalys progress bar for all processes according to execution order

        The user can choose to skip the animation in case they anticipate it being too long
        """

        #Skip animation if checkbox selected
        if st.session_state.skip_animation:
            return
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text(f"Running process {process.process_number}...")

        if run_time is None:
            #Determines animation time for FCFS and SJF
            animation_time = process.burst_time * 0.2
            completed_time = process.burst_time

        else:
            #Determines animation time for RR
            animation_time = run_time * 0.2
            completed_time = run_time

        #Updates progress bar gradually
        for percent in range(0, 101, 20):
            progress_bar.progress(percent)
            time.sleep(animation_time / 10)

        if run_time is None:
            #Displays success message for completion of process for FCFS and SJF
            st.success(f"Process {process.process_number} has been completed in {process.burst_time} second(s).\n")

        else:
            #Displays success message for completion for Round Robin
            if completed:
                st.success(f"Process {process.process_number} has been completed in {process.burst_time} second(s).\n")
            #Displays info message for time slice executed for Round Robin
            else:
                st.info(f"Process {process.process_number} has been executed for {completed_time} second(s).\n")

    def display_gantt_chart(self):
        """
        Displays Gantt chart 

        Uses timeline lists containing start and finish time to generate chart
        """
        fig = go.Figure()

        #colours assigned to distinguish between different processes
        colors = [
            "lightblue",
            "violet",
            "purple",
            "pink",
            "gray"
        ]

        for i, block in enumerate(self.timeline):

            #Calculates duration of every block

            duration = block["Finish"] - block["Start"]

            #Blocks for idle time
            if block["Process"] == "Idle":
                color = "lightgray"
                label = "Idle"
            
            #Block for normal processes looping through different colours
            else:
                color = colors[i % len(colors)]
                label = f"P{block['Process']}"

            #Creates horizontal bar on the same row
            fig.add_trace(
                go.Bar(
                    x=[duration],
                    y=["CPU"],                 
                    base=[block["Start"]],     
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
        
        #Collects time points of start and finish for x-axis labels
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

    def display_results(self, rr=False, run_time=None, completed_status=None):
        """
        Displays progress bars and results table in real time

        """
        
        #Prevents display when running again in history page
        if self.silent:
            return
        
        for index, process in enumerate(self.execution_order):

            #Round Robin uses time slices
            if rr:
                self.progress_of_process(process, run_time[index], completed_status[index])
            else:
                self.progress_of_process(process)
            
            #Stores results for all processes
            self.results.append({
            "Process Number": process.process_number,
            "Arrival Time": process.arrival_time,
            "Burst Time": process.burst_time,
            "Waiting Time": process.waiting_time,
            "Turnaround Time": process.turnaround_time
            })

            #Display table
            df = pd.DataFrame(self.results)
            self.table_placeholder.dataframe(df)

        #Display Gantt chart    
        self.display_gantt_chart()

    def get_summary_table(self):
        """
        Creates summary table with values and averages
        """
        summary =[]
        for process in self.processes:            
            summary.append({
            "Process Number": process.process_number,
            "Arrival Time": process.arrival_time,
            "Burst Time": process.burst_time,
            "Waiting Time": f"{process.waiting_time:.2f}",
            "Turnaround Time": f"{process.turnaround_time:.2f}"
            })

        #Adds a row for average
        summary.append({
        "Process Number": "Average",
        "Arrival Time": "-",
        "Burst Time": "-",
        "Waiting Time": f"{self.calculate_average_waiting_time():.2f}",
        "Turnaround Time": f"{self.calculate_average_turnaround_time():.2f}"
        })

        return summary

        

class ProcessThread(threading.Thread):
    """
    Thread class used for Round Robin

    Allows several time slices to run without two processes using the CPU at the same time
    """
    def __init__(self, process, run_time, cpu_lock):
        super().__init__()
        self.process = process
        self.run_time = run_time
        
        #Ensures the CPU is locked while one process is using it
        self.cpu_lock = cpu_lock

    def run(self):
        """
        Executes process using time slices
        """
        with self.cpu_lock:
            for i in range(self.run_time):
                time.sleep(1)
                #Reduces remaining burst time
                self.process.remaining_time -= 1
 
class RandomGenerator:
    """
    Generates radom arrival times and burst times as input
    """
    def generate_random_processes(num_processes, max_arrival=20, max_burst=20):
        processes = []
        for i in range(num_processes):
            processes.append({
                "Process Number": (i+1),
                "Arrival Time": random.randint(0, max_arrival),
                "Burst Time": random.randint(1, max_burst)
            })  
        return processes
