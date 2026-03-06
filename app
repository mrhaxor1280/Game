import streamlit as st
import random

players = ["Ali", "Sara", "Ahmed", "Ayesha"]

if "positions" not in st.session_state:
    st.session_state.positions = {p:1 for p in players}
    st.session_state.turn = 0
    st.session_state.papers = [1,2,2,3,-1,-1,-2,-2]

st.title("Race to 16 Game")

for p in players:
    st.write(f"{p}: {st.session_state.positions[p]} / 16")

if st.button("Play Turn"):

    current_player = players[st.session_state.turn % 4]

    if st.session_state.papers:
        paper = random.choice(st.session_state.papers)
        st.session_state.papers.remove(paper)

        st.session_state.positions[current_player] += paper
        st.write(f"{current_player} picked {paper}")

    for p in players:
        if p != current_player:
            st.session_state.positions[p] += 1

    for p in players:
        if st.session_state.positions[p] >= 16:
            st.success(f"{p} Wins!")
            st.stop()

    st.session_state.turn += 1
