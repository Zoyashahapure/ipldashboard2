import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.environ['STREAMLIT_CONFIG_DIR'] = os.path.join(os.path.expanduser("~"), ".streamlit")

st.title("IPL Data Analysis Dashboard")

# ---------- Load Data ----------
@st.cache_data
def load_data(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"
    return pd.read_csv(url)

# Replace with your own file IDs from Google Drive
matches_file_id = "1ZCqwqbFRHdwHTCO4LWQezWB99LfynPJB"
deliveries_file_id = "1kQXChtwZxkYrbzvVY5k4s-ffs6dVCVXK"

matches = load_data(matches_file_id)
deliveries = load_data(deliveries_file_id)

# ---------- Search Bar ----------
query = st.text_input("Enter your query (e.g., top 5 teams, top batsmen):")

if query:
    if "top 5 teams" in query.lower():
        # Top 5 teams by wins
        team_wins = matches['winner'].value_counts().head(5)
        plt.figure(figsize=(10,5))
        team_wins.plot(kind='bar', color='red')
        plt.title("Top 5 Teams by Wins")
        plt.ylabel("Number of Wins")
        plt.xlabel("Team")
        st.pyplot(plt)  # use Streamlit to display matplotlib plot

    elif "top batsmen" in query.lower():
        # Top 10 run scorers
        top_scorers = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
        plt.figure(figsize=(10,5))
        sns.barplot(x=top_scorers.values, y=top_scorers.index, color="yellow")
        plt.title("Top 10 Run Scorers in IPL")
        st.pyplot(plt)

    else:
        st.warning("Query not recognized. Try: 'top 5 teams', 'top batsmen'.")
