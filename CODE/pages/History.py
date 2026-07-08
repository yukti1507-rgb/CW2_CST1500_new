import streamlit as st
import pandas as pd

from history_database.db import get_connection, create_history_table

st.title("History of CPU Scheduling Algorithms")

conn = get_connection()

history = create_history_table()

df = pd.read_sql_query("SELECT * FROM history ORDER BY timestamp DESC", conn)

st.dataframe(df)

conn.close()

