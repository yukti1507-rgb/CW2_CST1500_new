import streamlit as st
from history_database.db import get_specific_identifier, get_specific_algorithm, get_specific_timestamp, delete_run
from logic.scheduler_logic import Process
from logic.FCFS_logic import FCFS_Scheduler
from logic.SJF_logic import SJF_Scheduler
from logic.RR_logic import RR_Scheduler

st.set_page_config(page_title= "History", page_icon= "📜", layout= "wide")
st.title("History of CPU Scheduling Algorithms")

#Ask user for their ID or username
identifier = st.text_input("Enter your Anonymous ID or Username to view your past runs:")

if identifier:
    algorithm_choice = st.selectbox(
        "Choose which algorithm history to view:",
        ["FCFS", "SJF", "RR"])
     
    #Retrieve all the stored runs for the algorithm
    df = get_specific_algorithm(identifier, algorithm_choice)

    #Checks in case user does not exist or input is missplelled
    if df.empty:
        st.warning("No history found for this ID or username.")
    else:
        st.success(f"Showing history for: {identifier}")
       
        st.subheader("Results table for Past Runs")
        #Display results table if selected
        show_table = st.checkbox("Show results table")
        if show_table:
            st.dataframe(df)
        
        st.subheader("Gantt Charts for Past Runs")
    
        #Separate runs according to timestamps
        grouped = df.groupby("timestamp")

        for timestamp, group in grouped:
            st.write(f"Run at {timestamp}")
            #Show Gantt chart by timestamps if selected
            show_chart = st.checkbox(f"Show Gantt Chart for run at {timestamp}")

            if show_chart:
                group = group[group["arrival_time"] >= 0]

                #Recreate list of stored data to rerun algorithm
                processes = []
                for _, row in group.iterrows():
                    processes.append(Process(
                        row["process_number"],
                        row["arrival_time"],
                        row["burst_time"]
                    ))

                #Use appropriate scheduler according to algorithm chosen
                if algorithm_choice == "FCFS":
                    scheduler = FCFS_Scheduler()
                elif algorithm_choice == "SJF":
                    scheduler = SJF_Scheduler()
                else:
                    st.info("The history is reconstructed using the default Round Robin time quantum 2.")
                    scheduler = RR_Scheduler(time_quantum=2)

                for p in processes:
                    scheduler.add_process(p)

                #Run processes without displaying progress bars and results table
                scheduler.silent = True
                scheduler.run()

                scheduler.display_gantt_chart()
            
            # Allow the user to download CSV file for selected run
            run_df = get_specific_timestamp(identifier, timestamp)
            csv = run_df.to_csv(index=False)
            st.download_button(
                label=f"Download CSV for run at {timestamp}",
                data=csv,
                file_name=f"{algorithm_choice}_run_{timestamp}.csv",
                mime="text/csv"
            )

            # Allow user to delete selected run
            if st.button(f"Delete run at {timestamp}"):
                delete_run(identifier, timestamp)            
                st.rerun()
