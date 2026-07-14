import streamlit as st
from history_database.db import get_specific_identifier, get_specific_algorithm, get_specific_timestamp, delete_run
from logic.scheduler_logic import Process
from logic.FCFS_logic import FCFS_Scheduler
from logic.SJF_logic import SJF_Scheduler
from logic.RR_logic import RR_Scheduler

st.title("History of CPU Scheduling Algorithms")


identifier = st.text_input("Enter your Anonymous ID or Username to view your past runs:")

if identifier:
    algorithm_choice = st.selectbox(
        "Choose which algorithm history to view:",
        ["FCFS", "SJF", "RR", "All"])
    
    if algorithm_choice == "All":
        df = get_specific_identifier(identifier)
    else:
        df = get_specific_algorithm(identifier, algorithm_choice)




    if df.empty:
        st.warning("No history found for this ID or username.")
    else:
        st.success(f"Showing history for: {identifier}")
       
        show_table = st.checkbox("Show results table")
        if show_table:
            st.dataframe(df)
        
        # Compare past runs chart
        st.subheader("Compare My Past Runs")
        compare_df = df.groupby("timestamp").agg({
            "waiting_time": "mean",
            "turnaround_time": "mean"
        }).reset_index()

        st.line_chart(compare_df.set_index("timestamp"))

        st.subheader("Gantt Charts for Past Runs")
    
        grouped = df.groupby("timestamp")

        for timestamp, group in grouped:
            st.write(f"Run at {timestamp}")
            show_chart = st.checkbox(f"Show Gantt Chart for run at {timestamp}")

            if show_chart:
                processes = []
                for _, row in group.iterrows():
                    processes.append(Process(
                        row["process_number"],
                        row["arrival_time"],
                        row["burst_time"]
                    ))

                if algorithm_choice == "FCFS":
                    scheduler = FCFS_Scheduler()
                elif algorithm_choice == "SJF":
                    scheduler = SJF_Scheduler()
                else:
                    scheduler = RR_Scheduler(time_quantum=4)

                for p in processes:
                    scheduler.add_process(p)

                scheduler.silent = True
                scheduler.run()

                scheduler.display_gantt_chart()
            
            # Download CSV for this run
            run_df = get_specific_timestamp(identifier, timestamp)
            csv = run_df.to_csv(index=False)
            st.download_button(
                label=f"Download CSV for run at {timestamp}",
                data=csv,
                file_name=f"{algorithm_choice}_run_{timestamp}.csv",
                mime="text/csv"
            )

            # Delete run
            if st.button(f"Delete run at {timestamp}"):
                delete_run(identifier, timestamp)
                st.warning("Run deleted. Refresh the page to update.")