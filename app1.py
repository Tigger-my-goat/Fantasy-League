import streamlit as st
import json
import os

DB_FILE = "fantasy_db.json"

# Player pool across Big 5 & UCL with season points
PLAYERS = {
    "Forwards": {
        "Erling Haaland (Man City)": 14,
        "Kylian Mbappé (Real Madrid)": 12,
        "Harry Kane (Bayern)": 11,
        "Mohamed Salah (Liverpool)": 10,
        "Vinícius Júnior (Real Madrid)": 9,
        "Robert Lewandowski (Barcelona)": 8
    },
    "Midfielders": {
        "Jude Bellingham (Real Madrid)": 11,
        "Florian Wirtz (Leverkusen)": 10,
        "Bukayo Saka (Arsenal)": 9,
        "Kevin De Bruyne (Man City)": 8,
        "Jamal Musiala (Bayern)": 8,
        "Rodri (Man City)": 6
    },
    "Defenders": {
        "Virgil van Dijk (Liverpool)": 7,
        "William Saliba (Arsenal)": 7,
        "Trent Alexander-Arnold (Liverpool)": 8,
        "Achraf Hakimi (PSG)": 6,
        "Alphonso Davies (Bayern)": 5
    },
    "Goalkeepers": {
        "Thibaut Courtois (Real Madrid)": 6,
        "Alisson Becker (Liverpool)": 6,
        "Gianluigi Donnarumma (PSG)": 5,
        "Manuel Neuer (Bayern)": 5
    }
}

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"leagues": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

st.set_page_config(page_title="Big 5 & UCL Fantasy", page_icon="⚽")
st.title("⚽ Big 5 & UCL Fantasy Hub")
db = load_db()

invite_code = st.query_params.get("code")

# 1. CREATE LEAGUE VIEW
if not invite_code:
    st.subheader("Create a League")
    league_name = st.text_input("League Name")
    tournament = st.selectbox("Tournament", ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "Champions League"])
    creator_name = st.text_input("Your Manager Name")

    if st.button("Create League") and league_name and creator_name:
        code = str(abs(hash(league_name)))[:6]
        db["leagues"][code] = {
            "name": league_name,
            "tournament": tournament,
            "members": {creator_name: {"squad": [], "points": 0}}
        }
        save_db(db)
        st.query_params["code"] = code
        st.rerun()

# 2. LEAGUE DASHBOARD & SQUAD BUILDING VIEW
else:
    league = db["leagues"].get(invite_code)
    if league:
        st.header(f"League: {league['name']}")
        st.caption(f"Competition: {league['tournament']}")
        st.info("💡 Share your browser URL with friends so they can join this league!")

        # Select or Add Manager Identity
        existing_managers = list(league["members"].keys())
        active_manager = st.selectbox("Select Your Manager Profile:", ["-- New Manager --"] + existing_managers)

        if active_manager == "-- New Manager --":
            new_name = st.text_input("Enter New Manager Name to Join:")
            if st.button("Join League") and new_name:
                if new_name not in league["members"]:
                    league["members"][new_name] = {"squad": [], "points": 0}
                    save_db(db)
                    st.success(f"Welcome {new_name}! Now pick your squad below.")
                    st.rerun()
        else:
            manager_data = league["members"][active_manager]
            
            # Squad Builder Form
            st.divider()
            st.subheader(f"📋 Manager: {active_manager}")
            
            if not manager_data["squad"]:
                st.write("Pick 1 player from each position to build your starting line-up:")
                
                fwd = st.selectbox("Select Forward", list(PLAYERS["Forwards"].keys()))
                mid = st.selectbox("Select Midfielder", list(PLAYERS["Midfielders"].keys()))
                dfe = st.selectbox("Select Defender", list(PLAYERS["Defenders"].keys()))
                gk = st.selectbox("Select Goalkeeper", list(PLAYERS["Goalkeepers"].keys()))

                if st.button("Save & Submit Squad"):
                    selected_squad = [fwd, mid, dfe, gk]
                    
                    # Calculate total squad score from preset match points
                    total_pts = 0
                    for category in PLAYERS.values():
                        for player, pts in category.items():
                            if player in selected_squad:
                                total_pts += pts

                    manager_data["squad"] = selected_squad
                    manager_data["points"] = total_pts
                    save_db(db)
                    st.success("Squad saved successfully!")
                    st.rerun()
            else:
                st.write("**Your Selected Squad:**")
                for p in manager_data["squad"]:
                    st.markdown(f"- ⚽ {p}")

        # LEADERBOARD TABLE
        st.divider()
        st.subheader("🏆 League Leaderboard")
        
        # Sort managers by points high-to-low
        sorted_members = sorted(
            league["members"].items(), 
            key=lambda item: item[1]["points"], 
            reverse=True
        )

        for rank, (manager, stats) in enumerate(sorted_members, start=1):
            squad_text = ", ".join(stats["squad"]) if stats["squad"] else "No team selected yet"
            st.markdown(f"**#{rank} {manager}** — **{stats['points']} pts**")
            st.caption(f"Squad: {squad_text}")
    else:
        st.error("League not found. Check your invite link.")