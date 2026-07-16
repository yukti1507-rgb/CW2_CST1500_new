from logic.scheduler_logic import Scheduler, ProcessThread

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

            self.execution_order.append(process)

            # Run for quantum or remaining burst
            run_time = min(self.time_quantum, process.remaining_time)

            self.execution_time.append(run_time)

            start_time = self.current_time

            #Add threading
            thread = ProcessThread(process, run_time, self.cpu_lock)
            thread.start()
            thread.join()

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

        self.display_results(rr=True, run_time=self.execution_time)
        return self.processes