from logic.scheduler_logic import Scheduler

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

            self.execution_order.append(process)

            # Start time
            process.start_time = self.current_time

            # Run the process
            self.current_time += process.burst_time

            # Finish time
            process.finish_time = self.current_time

            # Waiting time
            process.waiting_time = process.start_time - process.arrival_time


            # Turnaround time
            process.turnaround_time = process.finish_time - process.arrival_time

            # Add to timeline
            self.timeline.append({
                "Process": process.process_number,
                "Start": process.start_time,
                "Finish": process.finish_time
            })

        self.display_results()
        return self.processes
