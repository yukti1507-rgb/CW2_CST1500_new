from logic.scheduler_logic import Scheduler

class FCFS_Scheduler(Scheduler):
    """
    Implements First Come First Served algorithm

    Processes are executed in order of arrival time
    """
    def __init__(self):
        """
        Inherits all methods from parent class
        """
        super().__init__()
    
    def run(self):
        # Sort processes in ascending order of arrival time
        self.processes.sort(key=lambda x: x.arrival_time)

        if not self.processes:
            return

        self.current_time = 0
        
        for process in self.processes:
            # If a process has not arrived yet, it is stored as CPU idle time
            if self.current_time < process.arrival_time:
                self.timeline.append({
                    "Process": "Idle",
                    "Start": self.current_time,
                    "Finish": process.arrival_time
                })
                self.current_time = process.arrival_time
            
            #Stores execution order for results display
            self.execution_order.append(process)

            #As soon as current time is equal to arrival time, the process starts
            process.start_time = self.current_time

            #The process runs for the entire burst time
            self.current_time += process.burst_time
            
            #Records when the process finishes
            process.finish_time = self.current_time
           
            #Waiting time
            process.waiting_time = process.start_time - process.arrival_time
            
            #Turnaround time
            process.turnaround_time = process.finish_time - process.arrival_time

            #Add to Gantt chart timeline
            self.timeline.append({
            "Process": process.process_number,
            "Start": process.start_time,
            "Finish": process.finish_time
            })
       
        #Displays progress bars, results table and Gantt chart
        self.display_results()
        return self.processes
