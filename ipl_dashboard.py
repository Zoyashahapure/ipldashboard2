import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
os.environ['STREAMLIT_CONFIG_DIR'] = os.path.join(os.path.expanduser("~"), ".streamlit")

st.title("IPL Data Analysis Dashboard")

# ---------- Load Data ----------
@st.cache_data
def load_data(file_id, filename):
    url = f"https://drive.google.com/uc?id={file_id}"
    return pd.read_csv(url)

# Replace with your own file IDs from Google Drive
matches_file_id = "1ZCqwqbFRHdwHTCO4LWQezWB99LfynPJB"
deliveries_file_id = "1kQXChtwZxkYrbzvVY5k4s-ffs6dVCVXK"

matches = load_data(matches_file_id, "matches.csv")
deliveries = load_data(deliveries_file_id, "deliveries.csv")

# ---------- Search Bar ----------
query = st.text_input("Enter your query (e.g., top 5 teams, top 5 batsmen):")

if query:
    if "top 5 teams" in query.lower():
        team_wins = matches['winner'].value_counts().head(5)
        st.subheader("Top 5 Winning Teams")
        st.bar_chart(team_wins)

    elif "most winning team" in query.lower():
        most_wins = matches['winner'].value_counts().idxmax()
        st.success(f"The team with most wins is: {most_wins}")

    elif "top 5 batsmen" in query.lower():
        top_batsmen = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(5)
        st.subheader("Top 5 Batsmen (Total Runs)")
        st.bar_chart(top_batsmen)

    else:
        st.warning("Query not recognized. Try: 'top 5 teams', 'most winning team', 'top 5 batsmen'.")
