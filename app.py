import streamlit as st
import json
import os
import requests

DB_FILE = "fantasy_db.json"

# Helper functions to store multi-user data in a local file
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"leagues": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

st.title("⚽ Big 5 & UCL Fantasy Hub")
db = load_db()

# Read invite code from the URL parameter (?code=XXXX)
invite_code = st.query_params.get("code")

if not invite_code:
    # VIEW 1: League Creation Page
    st.subheader("Create a League")
    league_name = st.text_input("League Name")
    tournament = st.selectbox("Tournament", ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "Champions League"])
    creator_name = st.text_input("Your Manager Name")

    if st.button("Create League") and league_name and creator_name:
        code = str(abs(hash(league_name)))[:6]
        db["leagues"][code] = {
            "name": league_name,
            "tournament": tournament,
            "members": {creator_name: {"points": 0}}
        }
        save_db(db)
        st.query_params["code"] = code
        st.rerun()

else:
    # VIEW 2: Multiplayer League Dashboard (Shared via Link)
    league = db["leagues"].get(invite_code)
    if league:
        st.header(f"League: {league['name']}")
        st.caption(f"Competition: {league['tournament']}")
        st.info("Copy your browser URL to invite friends!")

        # Join League Form for Friends
        new_manager = st.text_input("Join this league — Enter Manager Name:")
        if st.button("Join") and new_manager:
            if new_manager not in league["members"]:
                league["members"][new_manager] = {"points": 0}
                save_db(db)
                st.success(f"{new_manager} joined!")
                st.rerun()

        # Real-Time Leaderboard Table
        st.subheader("Leaderboard")
        for manager, stats in league["members"].items():
            st.write(f"🏆 **{manager}**: {stats['points']} pts")