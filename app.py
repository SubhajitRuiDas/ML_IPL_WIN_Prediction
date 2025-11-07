import streamlit as st
import pickle
import pandas as pd
import os


teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
]

cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru'
]


team_colors = {
    'Sunrisers Hyderabad': '#FF822A',
    'Mumbai Indians': '#045093',
    'Royal Challengers Bangalore': '#DA1818',
    'Kolkata Knight Riders': '#3B0066',
    'Kings XI Punjab': '#B71C1C',
    'Chennai Super Kings': '#F9D71C',
    'Rajasthan Royals': '#EA1A8E',
    'Delhi Capitals': '#17449B'
}


pipe = pickle.load(open('pipe.pkl', 'rb'))


st.set_page_config(page_title="IPL Win Predictor", page_icon="🏏", layout="wide")


st.markdown(
    "<h1 style='text-align:center; color:#2E86C1;'>🏏 IPL WIN PREDICTOR DASHBOARD</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("🏆 Select Batting Team", sorted(teams))
    st.markdown(f"<h4 style='color:{team_colors[batting_team]};'>Batting Team</h4>", unsafe_allow_html=True)
    logo_path_bat = f"logos/{batting_team}.png"
    if os.path.exists(logo_path_bat):
        st.image(logo_path_bat, width=200)

with col2:
    bowling_team = st.selectbox("🔥 Select Bowling Team", sorted(teams))
    st.markdown(f"<h4 style='color:{team_colors[bowling_team]};'>Bowling Team</h4>", unsafe_allow_html=True)
    logo_path_bowl = f"logos/{bowling_team}.png"
    if os.path.exists(logo_path_bowl):
        st.image(logo_path_bowl, width=200)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>📍 Match Information</h3>", unsafe_allow_html=True)

col_city, col_target = st.columns([2, 1])
with col_city:
    selected_city = st.selectbox("Select Match Venue (City)", sorted(cities))
with col_target:
    target = st.number_input("🎯 Target Runs", min_value=1, step=1)


st.markdown("<br>", unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input("🏏 Current Score", min_value=0, step=1)
with col4:
    overs = st.number_input("⏱️ Overs Completed", min_value=0.0, max_value=20.0, step=0.1)
with col5:
    wickets = st.number_input("🚨 Wickets Out", min_value=0, max_value=10, step=1)


st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔮 Predict Win Probability", use_container_width=True)


if predict_btn:
    
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets_left],
        'total_runs_x': [target],
        'curr': [crr],
        'rrr': [rrr]
    })

    
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>🏁 MATCH PREDICTION RESULT</h2>", unsafe_allow_html=True)

    colA, colB, colC = st.columns([2, 1, 2])
    with colA:
        if os.path.exists(logo_path_bat):
            st.image(logo_path_bat, width=180)
        st.markdown(f"<h3 style='color:{team_colors[batting_team]};'>{batting_team}</h3>", unsafe_allow_html=True)
        st.progress(float(win))
        st.markdown(f"<b>Winning Probability:</b> {round(win * 100)}%")

    with colB:
        st.markdown("<h2 style='text-align:center;'>VS</h2>", unsafe_allow_html=True)

    with colC:
        if os.path.exists(logo_path_bowl):
            st.image(logo_path_bowl, width=180)
        st.markdown(f"<h3 style='color:{team_colors[bowling_team]};'>{bowling_team}</h3>", unsafe_allow_html=True)
        st.progress(float(loss))
        st.markdown(f"<b>Winning Probability:</b> {round(loss * 100)}%")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f"<h4 style='text-align:center;'>📊 {batting_team} need <b>{runs_left}</b> runs in <b>{balls_left}</b> balls with <b>{wickets_left}</b> wickets in hand.</h4>",
        unsafe_allow_html=True
    )

    st.balloons()