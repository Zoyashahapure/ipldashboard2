import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------- Styling ----------
st.markdown(r"""
<style>
.stApp {
    background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
    color: #2C2C2C;
}
h1 {
    color: #22223b;
    text-align: center;
    font-family: 'Helvetica', sans-serif;
}
</style>
""", unsafe_allow_html=True)

os.environ['STREAMLIT_CONFIG_DIR'] = os.path.join(os.path.expanduser("~"), ".streamlit")
st.title("IPL Data Analysis Dashboard")

# ---------- Load Data ----------
@st.cache_data
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

matches_url = "https://drive.google.com/uc?export=download&id=1ZCqwqbFRHdwHTCO4LWQezWB99LfynPJB"
deliveries_url = "https://drive.google.com/uc?export=download&id=1kQXChtwZxkYrbzvVY5k4s-ffs6dVCVXK"

matches = load_data(matches_url)
deliveries = load_data(deliveries_url)

if matches is None or deliveries is None:
    st.stop()

# ---------- Metrics ----------
col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", matches.shape[0])
col2.metric("Unique Teams", matches['team1'].nunique())
col3.metric("Unique Stadiums", matches['venue'].nunique())

# ---------- Analysis Option ----------
option = st.selectbox(
    "Choose analysis:",
    ["Select...", "Top 5 Teams", "Top Batsmen", "Top Stadiums", "Top Bowlers"]
)

if option != "Select...":
    
    # ----- Top 5 Teams -----
    if option == "Top 5 Teams":
        team_wins = matches['winner'].value_counts().head(5).reset_index()
        team_wins.columns = ['Team', 'Wins']
        fig = px.bar(team_wins, x='Team', y='Wins', color='Wins', text='Wins', title="Top 5 Teams by Wins")
        st.plotly_chart(fig, use_container_width=True)

    # ----- Top Batsmen -----
    elif option == "Top Batsmen":
        batsman_col = 'batsman' if 'batsman' in deliveries.columns else 'batter'
        top_scorers = deliveries.groupby(batsman_col)['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(top_scorers, x='batsman_runs', y=batsman_col, orientation='h',
                     color='batsman_runs', text='batsman_runs', title="Top 10 Run Scorers")
        st.plotly_chart(fig, use_container_width=True)

    # ----- Top Stadiums -----
    elif option == "Top Stadiums":
        stadium_wins = matches['venue'].value_counts().head(10).reset_index()
        stadium_wins.columns = ['Stadium', 'Matches']
        fig = px.bar(stadium_wins, x='Matches', y='Stadium', orientation='h',
                     color='Matches', text='Matches', title="Top 10 Stadiums by Matches")
        st.plotly_chart(fig, use_container_width=True)

    # ----- Top Bowlers -----
    elif option == "Top Bowlers":
        if 'player_dismissed' in deliveries.columns and 'bowler' in deliveries.columns:
            wickets = deliveries[deliveries['player_dismissed'].notnull()] \
                      .groupby('bowler').size().sort_values(ascending=False).head(5).reset_index()
            wickets.columns = ['Bowler', 'Wickets']
            fig = px.bar(wickets, x='Wickets', y='Bowler', orientation='h',
                         color='Wickets', text='Wickets', title="Top 5 Bowlers by Wickets")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Deliveries dataset missing required columns for bowlers.")
