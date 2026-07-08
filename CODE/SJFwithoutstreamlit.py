import streamlit as st
st.title("Shortest Job First(SJF)")
st.subheader("Enter number of processes:")
st.button("submit")


import pandas as pd
import time
#prompting user to input a value for num_processes 
#using a try/except loop in case user inputs a non-numeric value
def get_valid_integer(prompt):
    while True:
        user_input = input(prompt).strip()
        # Check if the user typed a decimal point
        if "." in user_input:
            print("Invalid input! Decimal values are not accepted.")
            continue 
        try:
            value = int(user_input)
            if value <= 0: 
                print("Invalid input! Only positive and non-zero values are accepted.")
            else:
                return value
        except ValueError:
            print("Invalid input! Please enter a valid whole number.")

def get_valid_float(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
            if value < 0:
                print("Invalid input! Negative values are not accepted.")
            else:
                return value 
        except ValueError:
            print("Invalid Input! Non-numeric values are not accepted.")


# Using get_valid_input function to prompt the user to enter a valid for thw number of processes
num_processes = get_valid_integer("Enter number of processes: ")

processes=[]
for i in range(int(num_processes)):
    burst_time=st.number_input(f"Enter burst time for process {i+1}", min_value=1, step=1)
    processes.append([i+1, burst_time])

#sorts the processes by shortest burst time 
processes.sort(key=lambda x: x[1])

waiting_time = 0
total_waiting_time = 0
total_turnaround_time = 0

results=[]

print("\nRunning processes in Shortest Job First order...\n")


for process in processes:
    process_num = process[0]
    burst_time = process[1]

    print(f"Process {process_num} is running...")
    time.sleep(burst_time)
    print(f"Process {process_num} has been completed in {burst_time} seconds.\n")
    turn_around_time = waiting_time + burst_time

    results.append([process_num, burst_time, waiting_time, turn_around_time])

    total_waiting_time += waiting_time
    total_turnaround_time += turn_around_time
    waiting_time += burst_time

print("\n")
print("  _______________________________________________________________")
print(" | Process Number | Burst Time | Waiting Time | Turn Around Time | ")
for result in results:
    process_num, burst_time, waiting_time, turn_around_time = result
    print(f" |   {process_num:<13}|",
        f"{burst_time:<10} |",
        f"{waiting_time:<12} |",
        f" {turn_around_time:<16}|")

average_waiting_time = total_waiting_time / num_processes
average_turnaround_time = total_turnaround_time / num_processes

print("\nAverage Waiting Time:", round(average_waiting_time, 2))
print("Average Turnaround Time:", round(average_turnaround_time, 2))





import streamlit as st
import time

st.title("SJF Scheduling Simulation")

# Create a progress bar placeholder
progress_bar = st.progress(0)
status_text = st.empty()

# Example: simulate 5 processes
for i in range(1, 6):
    status_text.text(f"Running process {i}...")
    for percent in range(0, 101, 20):  # increments of 20%
        progress_bar.progress(percent)
        time.sleep(0.2)  # delay to show progress
    st.success(f"Process {i} completed ✅")

status_text.text("All processes finished!")
