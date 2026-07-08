import threading
import time
# SHORTEST JOB FIRST 

#Defining the thread class 
class ProcessThread(threading.Thread):
    def __init__(self, pid, burst_time, arrival_time):
        super().__init__()
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0


class SJFScheduler:
    def __init__(self, processes):
        self.processes = processes
        self.current_time = 0
        self.results = []
        self.timeline =[] #records start/ finish times for visualisation (Gantt chart)


    def run(self, table_placeholder, st, time, pd):
        ready_queue = self.processes.copy()

        while ready_queue:
            available = [p for p in ready_queue if p.arrival_time <= self.current_time]

            if not available:
                self.current_time = min(p.arrival_time for p in ready_queue)
                available = [p for p in ready_queue if p.arrival_time <= self.current_time]

            # Sort by burst time, then arrival time
            available.sort(key=lambda p: (p.burst_time, p.arrival_time))
            process = available[0]
            ready_queue.remove(process)

            start_time = self.current_time
            # Calculate waiting_time, turnaround_time
            process.waiting_time = self.current_time - process.arrival_time
            process.turnaround_time = process.waiting_time + process.burst_time
            self.current_time += process.burst_time
            process.completion_time = self.current_time

            self.timeline.append({
                "Process": f"P{process.pid}",
                "Start": start_time,
                "Finish": process.completion_time
            })
            # Progress bar animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.text(f"Running process {process.pid}...")
            for percent in range(0, 101, 20):
                progress_bar.progress(percent)
                time.sleep(process.burst_time / 10)
            st.success(f"Process {process.pid} has been completed in {process.burst_time} second(s).\n")

            self.results.append(process)

            # Table will update, displaying each process after completion 
            df = pd.DataFrame(
                [[p.pid, p.arrival_time, p.burst_time, p.waiting_time, p.turnaround_time] for p in self.results],
                columns=["Process Number", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time"]
            )
            table_placeholder.table(df)
            time.sleep(2)

        return self.results, self.timeline

# ROUND ROBIN

# Defining the thread class
class ProcessThreadRobin(threading.Thread):
    def __init__(self, pid, burst_time, arrival_time):
        super().__init__()
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0

class RoundRobinScheduler:
    def __init__(self, processes, time_quantum):
        self.processes = processes
        self.time_quantum = time_quantum
        self.current_time = 0
        self.results = []
        self.timeline = []  # records start/finish times for Gantt chart

    def run(self, table_placeholder, st, time, pd):
        ready_queue = []
        processes = sorted(self.processes, key=lambda p: p.arrival_time)

        while processes or ready_queue:
            # Add newly arrived processes
            while processes and processes[0].arrival_time <= self.current_time:
                ready_queue.append(processes.pop(0))

            if ready_queue:
                process = ready_queue.pop(0)
                start_time = self.current_time

                # Run for quantum or remaining burst
                run_time = min(self.time_quantum, process.remaining_time)
                process.remaining_time -= run_time
                self.current_time += run_time

                # Progress bar animation
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_text.text(f"Running process {process.pid} for {run_time} second(s)...")
                for percent in range(0, 101, 20):
                    progress_bar.progress(percent)
                    time.sleep(run_time / 10)
                st.success(f"Process {process.pid} has been completed in {run_time} second(s).\n")

                # Timeline update
                self.timeline.append({
                    "Process": f"P{process.pid}",
                    "Start": start_time,
                    "Finish": self.current_time
                })

                if process.remaining_time > 0:
                    # Not finished, requeue
                    while processes and processes[0].arrival_time <= self.current_time:
                        ready_queue.append(processes.pop(0))
                    ready_queue.append(process)
                else:
                    # Finished
                    process.completion_time = self.current_time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    self.results.append(process)

                # Update table after each slice
                df = pd.DataFrame(
                    [[p.pid, p.arrival_time, p.burst_time, p.waiting_time, p.turnaround_time] for p in self.results],
                    columns=["Process Number", "Arrival Time", "Burst Time", "Waiting Time", "Turnaround Time"]
                )
                table_placeholder.table(df)
                time.sleep(2)

            else:
                # CPU idle until next arrival
                self.current_time = processes[0].arrival_time

        return self.results, self.timeline
