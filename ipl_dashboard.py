import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gdown
import os

os.environ['STREAMLIT_CONFIG_DIR'] = os.path.join(os.path.expanduser("~"), ".streamlit")

st.title("IPL Data Analysis Dashboard")

# ---------- Load Data ----------
@st.cache_data
def load_data(file_id, filename):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, filename, quiet=True)  # download CSV locally
    return pd.read_csv(filename)

# Replace with your own Google Drive file IDs
matches_file_id = "1ZCqwqbFRHdwHTCO4LWQezWB99LfynPJB"
deliveries_file_id = "1kQXChtwZxkYrbzvVY5k4s-ffs6dVCVXK"

matches = load_data(matches_file_id, "matches.csv")
deliveries = load_data(deliveries_file_id, "deliveries.csv")

# ---------- Search Bar ----------
query = st.text_input("Enter your query (e.g., top 5 teams, top batsmen):")

if query:
    if "top 5 teams" in query.lower():
        # Top 5 teams by wins
        team_wins = matches['winner'].value_counts().head(5)
        fig, ax = plt.subplots(figsize=(10,5))
        team_wins.plot(kind='bar', color='red', ax=ax)
        ax.set_title("Top 5 Teams by Wins")
        ax.set_ylabel("Number of Wins")
        ax.set_xlabel("Team")
        st.pyplot(fig)  # display matplotlib figure in Streamlit

    elif "top batsmen" in query.lower():
        # Top 10 run scorers
        top_scorers = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(x=top_scorers.values, y=top_scorers.index, ax=ax, color="yellow")
        ax.set_title("Top 10 Run Scorers in IPL")
        st.pyplot(fig)

    else:
        st.warning("Query not recognized. Try: 'top 5 teams', 'top batsmen'.")
