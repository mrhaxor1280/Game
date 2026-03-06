import streamlit as st
import random

st.set_page_config(page_title="Streamlit Ludo", layout="centered")

# --- GAME STATE ---
if "players" not in st.session_state:
    st.session_state.players = {
        "Red": {"pos": 0, "color": "#e74c3c"},
        "Blue": {"pos": 0, "color": "#3498db"},
        "Green": {"pos": 0, "color": "#2ecc71"},
        "Yellow": {"pos": 0, "color": "#f1c40f"},
    }

if "turn" not in st.session_state:
    st.session_state.turn = "Red"

if "dice" not in st.session_state:
    st.session_state.dice = None

# --- BOARD PATH (simplified 40 cells) ---
BOARD_SIZE = 40

# --- FUNCTIONS ---

def roll_dice():
    st.session_state.dice = random.randint(1, 6)


def move_player():
    player = st.session_state.turn
    steps = st.session_state.dice

    if steps is None:
        return

    st.session_state.players[player]["pos"] = (
        st.session_state.players[player]["pos"] + steps
    ) % BOARD_SIZE

    next_turn()


def next_turn():
    order = list(st.session_state.players.keys())
    i = order.index(st.session_state.turn)
    st.session_state.turn = order[(i + 1) % 4]


# --- UI ---
st.title("🎲 Streamlit Ludo Game (4 Players)")

st.write(f"**Current Turn:** {st.session_state.turn}")

col1, col2 = st.columns(2)

with col1:
    if st.button("Roll Dice"):
        roll_dice()

with col2:
    if st.button("Move Token"):
        move_player()

if st.session_state.dice:
    st.success(f"Dice rolled: {st.session_state.dice}")


# --- DRAW BOARD ---
board = ["" for _ in range(BOARD_SIZE)]

for name, data in st.session_state.players.items():
    pos = data["pos"]
    board[pos] += name[0]

st.subheader("Board")

rows = 8
cols = 5

for r in range(rows):
    cols_ui = st.columns(cols)
    for c in range(cols):
        i = r * cols + c
        if i < BOARD_SIZE:
            token = board[i]

            bg = "#ecf0f1"

            if "R" in token:
                bg = "#e74c3c"
            if "B" in token:
                bg = "#3498db"
            if "G" in token:
                bg = "#2ecc71"
            if "Y" in token:
                bg = "#f1c40f"

            cols_ui[c].markdown(
                f"""
                <div style='
                height:70px;
                border-radius:10px;
                background:{bg};
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:bold;
                font-size:20px;'>
                {token}
                </div>
                """,
                unsafe_allow_html=True,
            )


st.markdown("---")
st.write("Player Positions")

for p, d in st.session_state.players.items():
    st.write(p, "→", d["pos"])
