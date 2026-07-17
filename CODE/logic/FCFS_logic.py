from logic.scheduler_logic import Scheduler

class FCFS_Scheduler(Scheduler):
    def __init__(self):
        super().__init__()
    
    def run(self):
        self.processes.sort(key=lambda x: x.arrival_time)

        if not self.processes:
            return

        self.current_time = 0
        
        for process in self.processes:
            if self.current_time < process.arrival_time:
                self.timeline.append({
                    "Process": "Idle",
                    "Start": self.current_time,
                    "Finish": process.arrival_time
                })
                self.current_time = process.arrival_time
            
            self.execution_order.append(process)

            process.start_time = self.current_time

            self.current_time += process.burst_time
            process.finish_time = self.current_time
           
            process.waiting_time = round(process.start_time - process.arrival_time, 2)
            process.turnaround_time = round(process.finish_time - process.arrival_time, 2)

            self.timeline.append({
            "Process": process.process_number,
            "Start": process.start_time,
            "Finish": process.finish_time
            })
       
        self.display_results()
        return self.processes
