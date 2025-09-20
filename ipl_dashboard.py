import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
os.environ['STREAMLIT_CONFIG_DIR'] = os.path.join(os.path.expanduser("~"), ".streamlit")


st.title("My IPL Dashboard")


def load_data():
    # Replace with your Google Drive file ID
    file_id = "1ZCqwqbFRHdwHTCO4LWQezWB99LfynPJB"
    url = f"https://drive.google.com/file/d/1ZCqwqbFRHdwHTCO4LWQezWB99LfynPJB/view?usp=drive_link"
    return pd.read_csv(url)# Title
st.title("IPL Data Analysis Dashboard")

# Search Bar
query = st.text_input("Enter your query (e.g., top 5 teams):")

if query:
    if "top 5 teams" in query.lower():
        team_wins = matches['winner'].value_counts().head(5)

        st.subheader("Top 5 Winning Teams")
        fig, ax = plt.subplots()
        team_wins.plot(kind='bar', ax=ax, color="skyblue")
        plt.ylabel("Wins")
        plt.xlabel("Team")
        st.pyplot(fig)

    elif "most winning team" in query.lower():
        most_wins = matches['winner'].value_counts().idxmax()
        st.success(f"The team with most wins is: {most_wins}")

    else:
        st.warning("Query not recognized. Try: 'top 5 teams', 'most winning team'.")
