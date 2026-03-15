import streamlit as st
import random
import time

st.set_page_config(page_title="PowerDice X-Cross", page_icon="⭐", layout="wide")

# ────────────────────────────────────────────────
# SESSION STATE
# ────────────────────────────────────────────────

if "player_names" not in st.session_state:
    st.session_state.player_names = None

# ────────────────────────────────────────────────
# START SCREEN
# ────────────────────────────────────────────────

if st.session_state.player_names is None:

    st.title("⭐ POWER DICE X-CROSS")

    cols = st.columns(4)

    defaults = ["Player 1","Player 2","Player 3","Player 4"]
    names_input = []

    for i,col in enumerate(cols):
        with col:
            name = st.text_input(f"Player {i+1}",defaults[i])
            names_input.append(name)

    if st.button("START GAME",use_container_width=True):

        st.session_state.player_names = names_input
        st.session_state.positions = [1,1,1,1]
        st.session_state.current_turn = 0
        st.session_state.round = 1
        st.session_state.winner = None

        st.rerun()

    st.stop()

# ────────────────────────────────────────────────
# GAME VARIABLES
# ────────────────────────────────────────────────

names = st.session_state.player_names

colors = [
"#3b82f6",  # blue
"#f97316",  # orange
"#22c55e",  # green
"#ef4444"   # red
]

tokens = ["🔵","🟠","🟢","🔴"]

# ────────────────────────────────────────────────
# STYLE
# ────────────────────────────────────────────────

st.markdown("""
<style>

.board{
position:relative;
width:1000px;
height:720px;
margin:auto;
}

.arm{
position:absolute;
display:flex;
flex-direction:column;
gap:4px;
}

.row{
display:flex;
gap:4px;
}

.cell{
width:42px;
height:42px;
border-radius:6px;
border:2px solid black;
display:flex;
align-items:center;
justify-content:center;
font-weight:bold;
color:white;
font-size:13px;
}

.star{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
font-size:70px;
}

.player-name{
font-size:20px;
font-weight:bold;
text-align:center;
margin-bottom:6px;
}

</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# WIN SCREEN
# ────────────────────────────────────────────────

if st.session_state.winner:

    st.balloons()

    idx = names.index(st.session_state.winner)

    st.markdown(
        f"<h1 style='text-align:center;color:{colors[idx]};'>🏆 {st.session_state.winner} WINS!</h1>",
        unsafe_allow_html=True
    )

    if st.button("Play Again"):
        st.session_state.positions=[1,1,1,1]
        st.session_state.current_turn=0
        st.session_state.round=1
        st.session_state.winner=None
        st.rerun()

    st.stop()

# ────────────────────────────────────────────────
# PLAYER STATUS
# ────────────────────────────────────────────────

cols = st.columns(4)

for i,c in enumerate(cols):

    with c:

        pos = st.session_state.positions[i]

        st.markdown(
        f"<h3 style='color:{colors[i]};text-align:center'>{tokens[i]} {names[i]}</h3>",
        unsafe_allow_html=True)

        st.progress(pos/16)

# ────────────────────────────────────────────────
# BOARD FUNCTION
# ────────────────────────────────────────────────

def create_arm(player,angle,top,left):

    numbers=list(range(1,16))

    row1=numbers[:8]
    row2=numbers[8:]

    r1=""
    r2=""

    for n in row1:

        token = tokens[player] if st.session_state.positions[player]==n else ""

        r1+=f'<div class="cell" style="background:{colors[player]}">{n}{token}</div>'

    for n in row2:

        token = tokens[player] if st.session_state.positions[player]==n else ""

        r2+=f'<div class="cell" style="background:{colors[player]}">{n}{token}</div>'

    return f"""
    <div class="arm" style="top:{top};left:{left};transform:rotate({angle}deg);">

    <div class="player-name" style="color:{colors[player]}">
    {names[player]}
    </div>

    <div class="row">{r1}</div>
    <div class="row">{r2}</div>

    </div>
    """

# ────────────────────────────────────────────────
# DRAW BOARD
# ────────────────────────────────────────────────

board_html=f"""
<div class="board">

{create_arm(0,-45,"20%","5%")}
{create_arm(1,45,"20%","60%")}
{create_arm(2,-135,"62%","5%")}
{create_arm(3,135,"62%","60%")}

<div class="star">⭐</div>

</div>
"""

st.markdown(board_html,unsafe_allow_html=True)

# ────────────────────────────────────────────────
# TURN INFO
# ────────────────────────────────────────────────

turn = st.session_state.current_turn

st.markdown(
f"### Round {st.session_state.round} — Turn: **{names[turn]} {tokens[turn]}**"
)

# ────────────────────────────────────────────────
# DICE
# ────────────────────────────────────────────────

if st.button(f"ROLL DICE – {names[turn]}",use_container_width=True):

    placeholder = st.empty()

    for _ in range(8):

        v=random.choice([1,2,-1,-2])

        placeholder.markdown(f"# {v:+}")

        time.sleep(0.1)

    roll=random.choice([1,2,-1,-2])

    placeholder.markdown(f"# {roll:+}")

    # everyone +1

    for i in range(4):
        if st.session_state.positions[i] < 16:
            st.session_state.positions[i]+=1

    # power move

    pos=st.session_state.positions[turn]

    newpos=pos+roll

    if 1<=newpos<=16:
        st.session_state.positions[turn]=newpos

    # win check

    for i in range(4):
        if st.session_state.positions[i]==16:
            st.session_state.winner=names[i]

    st.session_state.current_turn=(turn+1)%4
    st.session_state.round+=1

    st.rerun()

# ────────────────────────────────────────────────
# RULES
# ────────────────────────────────────────────────

with st.expander("Rules"):

    st.write("""
• Each player path = **1 → 15 + ⭐ (16)**  
• Every round **all players move +1**  
• Active player rolls **+1 +2 −1 −2**  
• Must land **exactly on 16**  
• First player reaching ⭐ wins
""")
