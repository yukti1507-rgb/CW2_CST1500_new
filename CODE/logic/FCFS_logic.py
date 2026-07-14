from logic.scheduler_logic import Scheduler, ProcessThread

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
            

            process.start_time = self.current_time
            run_time = process.burst_time

            thread = ProcessThread(process, run_time, self.cpu_lock)
            thread.start()
            thread.join()

            self.current_time += run_time
            process.finish_time = self.current_time
           
            process.waiting_time = process.start_time - process.arrival_time
            process.turnaround_time = (process.finish_time + process.arrival_time)


            self.timeline.append({
            "Process": process.process_number,
            "Start": process.start_time,
            "Finish": process.finish_time
            })
        

       
        self.display_results()
        return self.processes, self.get_summary()