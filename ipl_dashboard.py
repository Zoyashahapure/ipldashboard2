import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Page Setup ----------
st.set_page_config(page_title="IPL Data Analysis Dashboard", layout="centered")

# ---------- Basic CSS ----------
st.markdown(r"""
<style>
.stApp {
    background: radial-gradient(circle, #f6d365 0%, #fda085 100%);
    color: #2C2C2C;
}
h1, h2 {
    color: #22223b;
    text-align: center;
    font-family: 'Helvetica', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
logo_url = "images.png"
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo_url, width=100)
with col2:
    st.markdown(
        "<h1 style='text-align:left;'>IPL Data Analysis Dashboard</h1>",
        unsafe_allow_html=True
    )

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

# ---------- Clean Data ----------
matches.drop_duplicates(inplace=True)
deliveries.drop_duplicates(inplace=True)
matches.fillna({'winner': 'No Result', 'venue': 'Unknown Venue'}, inplace=True)
deliveries['batsman_runs'].fillna(0, inplace=True)

# ---------- Metrics ----------
col1, col2, col3 = st.columns(3)
col1.markdown(f"🏏 **Total Matches**: {matches.shape[0]}")
col2.markdown(f"🌟 **Unique Teams**: {matches['team1'].nunique()}")
col3.markdown(f"🏟️ **Unique Stadiums**: {matches['venue'].nunique()}")

# ---------- Analysis Selection ----------
option = st.selectbox(
    "Choose analysis:",
    ["Select...", "Top 5 Teams", "Top Batsmen", "Top Stadiums",
     "Top Bowlers", "Most Sixes", "Most Fours", "Matches by City"]
)

# ---------- Display Analysis Based on Selection ----------
if option == "Top 5 Teams":
    team_wins = matches['winner'].value_counts().head(5).reset_index()
    team_wins.columns = ['Team', 'Wins']
    fig = px.bar(team_wins, x='Team', y='Wins', color='Wins', text='Wins',
                 title="🏆 Top 5 Teams by Wins", color_continuous_scale='Tealgrn')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Top Batsmen":
    bat_col = 'batsman' if 'batsman' in deliveries.columns else 'batter'
    top_scorers = (deliveries.groupby(bat_col)['batsman_runs']
                   .sum().sort_values(ascending=False).head(10).reset_index())
    fig = px.bar(top_scorers, x='batsman_runs', y=bat_col, orientation='h',
                 color='batsman_runs', text='batsman_runs',
                 title="🏏 Top 10 Run Scorers", color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Top Stadiums":
    stadium_wins = matches['venue'].value_counts().head(10).reset_index()
    stadium_wins.columns = ['Stadium', 'Matches']
    fig = px.bar(stadium_wins, x='Matches', y='Stadium', orientation='h',
                 color='Matches', text='Matches', color_continuous_scale='OrRd')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Most Sixes":
    bat_col = 'batsman' if 'batsman' in deliveries.columns else 'batter'
    sixes = deliveries[deliveries['batsman_runs'] == 6][bat_col].value_counts().head(10).reset_index()
    sixes.columns = ['Batsman', 'Sixes']
    fig = px.bar(sixes, x='Sixes', y='Batsman', orientation='h', color='Sixes',
                 text='Sixes', color_continuous_scale='Pinkyl')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Most Fours":
    bat_col = 'batsman' if 'batsman' in deliveries.columns else 'batter'
    fours = deliveries[deliveries['batsman_runs'] == 4][bat_col].value_counts().head(10).reset_index()
    fours.columns = ['Batsman', 'Fours']
    fig = px.bar(fours, x='Fours', y='Batsman', orientation='h', color='Fours',
                 text='Fours', color_continuous_scale='Sunset')
    st.plotly_chart(fig, use_container_width=True)

elif option == "Matches by City":
    city_count = matches['city'].value_counts().head(10).reset_index()
    city_count.columns = ['City', 'Matches']
    fig = px.pie(city_count, names='City', values='Matches',
                 title="🗺️ Matches Hosted per City")
    st.plotly_chart(fig, use_container_width=True)

elif option == "Top Bowlers":
    if 'player_dismissed' in deliveries.columns and 'bowler' in deliveries.columns:
        wickets = (deliveries[deliveries['player_dismissed'].notnull()]
                   .groupby('bowler').size().sort_values(ascending=False).head(5).reset_index())
        wickets.columns = ['Bowler', 'Wickets']
        fig = px.bar(wickets, x='Wickets', y='Bowler', orientation='h', color='Wickets',
                     text='Wickets', color_continuous_scale='Agsunset')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Deliveries dataset missing required columns for bowlers.")



