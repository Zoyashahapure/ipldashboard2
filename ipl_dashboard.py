import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
st.markdown(r"""
    <style>
    .stApp {
        background-color: #EBD9D1;  /* Light blue background */

    }
    </style>
    """, unsafe_allow_html=True)

os.environ['STREAMLIT_CONFIG_DIR'] = os.path.join(os.path.expanduser("~"), ".streamlit")

st.title("IPL Data Analysis Dashboard")

# ---------- Load Data ----------
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

# ---------- Google Drive direct download links ----------
matches_url = "https://drive.google.com/uc?export=download&id=1ZCqwqbFRHdwHTCO4LWQezWB99LfynPJB"
deliveries_url = "https://drive.google.com/uc?export=download&id=1kQXChtwZxkYrbzvVY5k4s-ffs6dVCVXK"

matches = load_data(matches_url)
deliveries = load_data(deliveries_url)

# Stop app if data failed to load
if matches is None or deliveries is None:
    st.stop()

# ---------- Search Bar ----------
query = st.text_input("Enter your query (e.g., top 5 teams, top batsmen, top stadiums, top bowlers):")

if query:
    q = query.lower()

    if "top 5 teams" in q:
        # Top 5 teams by wins
        team_wins = matches['winner'].value_counts().head(5)
        fig, ax = plt.subplots(figsize=(10,5))
        team_wins.plot(kind='bar', color='#5D688A', ax=ax)
        ax.set_title("Top 5 Teams by Wins")
        ax.set_ylabel("Number of Wins")
        ax.set_xlabel("Team")
        st.pyplot(fig)

    elif "top batsmen" in q or "top run scorers" in q:
        batsman_col = 'batsman' if 'batsman' in deliveries.columns else 'batter'
        top_scorers = deliveries.groupby(batsman_col)['batsman_runs'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(x=top_scorers.values, y=top_scorers.index, ax=ax, color="#B9375D")
        ax.set_title("Top 10 Run Scorers")
        ax.set_xlabel("Runs")
        ax.set_ylabel("Batsman")
        st.pyplot(fig)

    elif "top stadiums" in q:
        stadium_wins = matches['venue'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10,5))
        stadium_wins.plot(kind='bar', color='#007074', ax=ax)
        ax.set_title("Top 10 Stadiums by Number of Matches")
        ax.set_ylabel("Matches")
        ax.set_xlabel("Stadium")
        st.pyplot(fig)

    elif "top bowlers" in q or "top 5 bowlers" in q:
        if 'player_dismissed' in deliveries.columns and 'bowler' in deliveries.columns:
            wickets = deliveries[deliveries['player_dismissed'].notnull()].groupby('bowler').size().sort_values(ascending=False).head(5)
            fig, ax = plt.subplots(figsize=(10,5))
            wickets.plot(kind='bar', color='#FF6464', ax=ax)
            ax.set_title("Top 5 Bowlers by Wickets")
            ax.set_ylabel("Wickets")
            ax.set_xlabel("Bowler")
            st.pyplot(fig)
        else:
            st.warning("Deliveries dataset missing required columns for bowlers.")

    else:
        st.warning("Query not recognized. Try: 'top 5 teams', 'top batsmen', 'top stadiums', 'top bowlers'.")















