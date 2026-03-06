import streamlit as st
import random

st.title("Race to 16 Board Game")

players = ["Ali","Sara","Ahmed","Ayesha"]

if "positions" not in st.session_state:
    st.session_state.positions = [0,0,0,0]

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "jar" not in st.session_state:
    st.session_state.jar = [2,3,4,5,2,3,-1,-2]
    random.shuffle(st.session_state.jar)

current_player = st.session_state.turn % 4

st.write("Current Player:", players[current_player])

cols = st.columns(4)

for i in range(4):
    cols[i].metric(players[i], st.session_state.positions[i])

if st.button("Draw Paper / Play Turn"):

    if len(st.session_state.jar) > 0:
        move = st.session_state.jar.pop()
    else:
        move = 1

    st.session_state.positions[current_player] += move

    if st.session_state.positions[current_player] < 0:
        st.session_state.positions[current_player] = 0

    if st.session_state.positions[current_player] >= 16:
        st.success(players[current_player] + " Wins!")
        st.stop()

    st.session_state.turn += 1

st.write("Goal: Reach 16 first")
