import streamlit as st
import json
import os

DB_FILE = "fantasy_db.json"

st.set_page_config(page_title="Big 5 & UCL Fantasy", page_icon="⚽", layout="wide")

# Custom UI Styling
st.markdown("""
<style>
    .stApp { background-color: #0f172a; }
    .player-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    .player-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 2px solid #38bdf8;
        object-fit: cover;
    }
    .stat-tag {
        background-color: #0f172a;
        color: #38bdf8;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 2px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Comprehensive League Player Pool with Stats & Avatars
PLAYER_DATABASE = {
    "La Liga": {
        "Goalkeepers": [
            {"name": "Thibaut Courtois", "club": "Real Madrid", "rating": 89, "goals": 0, "assists": 0, "clean_sheets": 8, "pts": 42, "img": "https://img.a.transfermarkt.technology/portrait/header/108390-1665063857.jpg"},
            {"name": "Jan Oblak", "club": "Atlético Madrid", "rating": 88, "goals": 0, "assists": 0, "clean_sheets": 7, "pts": 38, "img": "https://img.a.transfermarkt.technology/portrait/header/121483-1684311893.jpg"},
            {"name": "Marc-André ter Stegen", "club": "Barcelona", "rating": 89, "goals": 0, "assists": 0, "clean_sheets": 6, "pts": 34, "img": "https://img.a.transfermarkt.technology/portrait/header/74857-1665063673.jpg"},
            {"name": "Unai Simón", "club": "Athletic Club", "rating": 84, "goals": 0, "assists": 0, "clean_sheets": 5, "pts": 30, "img": "https://img.a.transfermarkt.technology/portrait/header/271571-1665063782.jpg"}
        ],
        "Defenders": [
            {"name": "Antonio Rüdiger", "club": "Real Madrid", "rating": 87, "goals": 2, "assists": 1, "clean_sheets": 8, "pts": 51, "img": "https://img.a.transfermarkt.technology/portrait/header/86202-1665063518.jpg"},
            {"name": "Jules Koundé", "club": "Barcelona", "rating": 85, "goals": 1, "assists": 3, "clean_sheets": 7, "pts": 46, "img": "https://img.a.transfermarkt.technology/portrait/header/411975-1665063806.jpg"},
            {"name": "Dani Carvajal", "club": "Real Madrid", "rating": 86, "goals": 1, "assists": 4, "clean_sheets": 7, "pts": 48, "img": "https://img.a.transfermarkt.technology/portrait/header/138927-1665063462.jpg"},
            {"name": "Ronald Araújo", "club": "Barcelona", "rating": 86, "goals": 1, "assists": 0, "clean_sheets": 6, "pts": 38, "img": "https://img.a.transfermarkt.technology/portrait/header/480267-1665063740.jpg"},
            {"name": "Robin Le Normand", "club": "Atlético Madrid", "rating": 83, "goals": 1, "assists": 1, "clean_sheets": 6, "pts": 36, "img": "https://img.a.transfermarkt.technology/portrait/header/354060-1665063712.jpg"},
            {"name": "Pau Cubarsí", "club": "Barcelona", "rating": 81, "goals": 0, "assists": 1, "clean_sheets": 5, "pts": 31, "img": "https://img.a.transfermarkt.technology/portrait/header/922240-1708332152.jpg"}
        ],
        "Midfielders": [
            {"name": "Jude Bellingham", "club": "Real Madrid", "rating": 90, "goals": 9, "assists": 6, "clean_sheets": 0, "pts": 74, "img": "https://img.a.transfermarkt.technology/portrait/header/581678-1693987944.jpg"},
            {"name": "Pedri", "club": "Barcelona", "rating": 86, "goals": 4, "assists": 5, "clean_sheets": 0, "pts": 52, "img": "https://img.a.transfermarkt.technology/portrait/header/683840-1665063628.jpg"},
            {"name": "Federico Valverde", "club": "Real Madrid", "rating": 88, "goals": 5, "assists": 4, "clean_sheets": 0, "pts": 58, "img": "https://img.a.transfermarkt.technology/portrait/header/369081-1665063574.jpg"},
            {"name": "Dani Olmo", "club": "Barcelona", "rating": 85, "goals": 6, "assists": 2, "clean_sheets": 0, "pts": 49, "img": "https://img.a.transfermarkt.technology/portrait/header/293385-1665063600.jpg"},
            {"name": "Luka Modrić", "club": "Real Madrid", "rating": 86, "goals": 2, "assists": 5, "clean_sheets": 0, "pts": 41, "img": "https://img.a.transfermarkt.technology/portrait/header/27992-1665063428.jpg"},
            {"name": "Frenkie de Jong", "club": "Barcelona", "rating": 87, "goals": 2, "assists": 3, "clean_sheets": 0, "pts": 39, "img": "https://img.a.transfermarkt.technology/portrait/header/326330-1665063650.jpg"}
        ],
        "Forwards": [
            {"name": "Kylian Mbappé", "club": "Real Madrid", "rating": 91, "goals": 14, "assists": 4, "clean_sheets": 0, "pts": 92, "img": "https://img.a.transfermarkt.technology/portrait/header/342229-1682683695.jpg"},
            {"name": "Vinícius Júnior", "club": "Real Madrid", "rating": 90, "goals": 12, "assists": 7, "clean_sheets": 0, "pts": 88, "img": "https://img.a.transfermarkt.technology/portrait/header/371998-1665063548.jpg"},
            {"name": "Lamine Yamal", "club": "Barcelona", "rating": 87, "goals": 8, "assists": 9, "clean_sheets": 0, "pts": 82, "img": "https://img.a.transfermarkt.technology/portrait/header/937958-1708332115.jpg"},
            {"name": "Robert Lewandowski", "club": "Barcelona", "rating": 88, "goals": 15, "assists": 3, "clean_sheets": 0, "pts": 89, "img": "https://img.a.transfermarkt.technology/portrait/header/38253-1701111622.jpg"},
            {"name": "Antoine Griezmann", "club": "Atlético Madrid", "rating": 87, "goals": 7, "assists": 6, "clean_sheets": 0, "pts": 64, "img": "https://img.a.transfermarkt.technology/portrait/header/125781-1684311855.jpg"},
            {"name": "Nico Williams", "club": "Athletic Club", "rating": 85, "goals": 5, "assists": 5, "clean_sheets": 0, "pts": 53, "img": "https://img.a.transfermarkt.technology/portrait/header/709187-1665063760.jpg"}
        ]
    }
}

# Fallback pool for other leagues
DEFAULT_POOL = PLAYER_DATABASE["La Liga"]

def get_league_players(tournament_name):
    return PLAYER_DATABASE.get(tournament_name, DEFAULT_POOL)

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"leagues": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

st.title("⚽ Big 5 & Champions League Fantasy Hub")
db = load_db()

invite_code = st.query_params.get("code")

# VIEW 1: CREATE LEAGUE
if not invite_code:
    st.subheader("🏆 Create New Fantasy League")
    col1, col2 = st.columns(2)
    with col1:
        league_name = st.text_input("League Name")
        tournament = st.selectbox("Tournament", ["La Liga", "Premier League", "Champions League", "Serie A", "Bundesliga", "Ligue 1"])
    with col2:
        creator_name = st.text_input("Your Manager Name")

    if st.button("Create League") and league_name and creator_name:
        code = str(abs(hash(league_name)))[:6]
        db["leagues"][code] = {
            "name": league_name,
            "tournament": tournament,
            "members": {creator_name: {"squad": {}, "points": 0}}
        }
        save_db(db)
        st.query_params["code"] = code
        st.rerun()

# VIEW 2: MULTIPLAYER DASHBOARD
else:
    league = db["leagues"].get(invite_code)
    if league:
        st.header(f"League: {league['name']}")
        st.caption(f"Tournament: **{league['tournament']}** | Invite Code: `{invite_code}`")
        
        # Profile Selector
        managers = list(league["members"].keys())
        active_manager = st.selectbox("👤 Select Your Manager Profile:", ["-- Join as New Manager --"] + managers)

        if active_manager == "-- Join as New Manager --":
            new_name = st.text_input("Enter Manager Name to Join:")
            if st.button("Join League") and new_name:
                if new_name not in league["members"]:
                    league["members"][new_name] = {"squad": {}, "points": 0}
                    save_db(db)
                    st.success(f"{new_name} joined!")
                    st.rerun()
        else:
            mgr_data = league["members"][active_manager]
            pool = get_league_players(league["tournament"])

            tabs = st.tabs(["📋 Pick Starting 11", "🏆 Leaderboard", "📊 Player Stats Pool"])

            # TAB 1: FULL 11-PLAYER SQUAD BUILDER
            with tabs[0]:
                st.subheader("⚡ Pick Your Starting 11 (Formation: 4-4-2)")
                
                squad = mgr_data.get("squad", {})
                
                with st.form("squad_form"):
                    st.markdown("### 🧤 Goalkeeper (1)")
                    gk_names = [p["name"] for p in pool["Goalkeepers"]]
                    gk_selected = st.selectbox("GK", gk_names, index=0)

                    st.markdown("### 🛡️ Defenders (4)")
                    def_names = [p["name"] for p in pool["Defenders"]]
                    d1 = st.selectbox("Defender 1 (CB)", def_names, index=0)
                    d2 = st.selectbox("Defender 2 (CB)", def_names, index=min(1, len(def_names)-1))
                    d3 = st.selectbox("Defender 3 (LB)", def_names, index=min(2, len(def_names)-1))
                    d4 = st.selectbox("Defender 4 (RB)", def_names, index=min(3, len(def_names)-