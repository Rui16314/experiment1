import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Auction Dashboard", layout="wide")

st.title("🎯 Auction Game Dashboard")

# Connect to database
conn = sqlite3.connect('auction.db')
df = pd.read_sql_query("SELECT * FROM results", conn)

# Show raw data
with st.expander("📄 Raw Results Table"):
    st.dataframe(df)

# Select experiment
experiment = st.selectbox("Choose Experiment", sorted(df['experiment'].unique()))

filtered = df[df['experiment'] == experiment]

# Show earnings
st.subheader(f"💰 Earnings in Experiment {experiment}")
earnings = filtered.groupby('name')['payoff'].sum().reset_index()
st.dataframe(earnings)

# Plot bids vs. valuations
st.subheader("📊 Bids vs. Valuations")
st.scatter_chart(filtered[['valuation', 'bid']])

conn.close()
