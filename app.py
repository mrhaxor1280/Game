import streamlit as st
import random

st.set_page_config(layout="wide")

players = ["Ali","Sara","Ahmed","Ayesha"]

colors = {
    "Ali":"red",
    "Sara":"green",
    "Ahmed":"blue",
    "Ayesha":"orange"
}

if "pos" not in st.session_state:
    st.session_state.pos = {p:0 for p in players}
    st.session_state.turn = 0
    st.session_state.papers = [1,2,2,3,-1,-1,-2,-2]

st.title("🎯 Race To 16")

current_player = players[st.session_state.turn % 4]
st.write("Current Turn:", current_player)

if st.button("Play Turn"):

    if st.session_state.papers:

        paper = random.choice(st.session_state.papers)
        st.session_state.papers.remove(paper)

        st.session_state.pos[current_player] += paper

        st.success(f"{current_player} drew {paper}")

    for p in players:
        if p != current_player:
            st.session_state.pos[p] += 1

    st.session_state.turn += 1


size = 17
center = 8

board = [["" for _ in range(size)] for _ in range(size)]

def tile(color,text=""):
    return f"""
    <div style="
    width:35px;
    height:35px;
    background:{color};
    display:flex;
    align-items:center;
    justify-content:center;
    border:1px solid black;
    font-size:12px;
    ">
    {text}
    </div>
    """

html = ""

for r in range(size):

    html += "<div style='display:flex;'>"

    for c in range(size):

        cell_color = "#eee"
        text = ""

        if r == center and c == center:
            cell_color = "gold"
            text = "16"

        if c == center:
            cell_color = "#ffcccc"

        if r == center:
            cell_color = "#ccffcc"

        html += tile(cell_color,text)

    html += "</div>"

st.markdown(html, unsafe_allow_html=True)
