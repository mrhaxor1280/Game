import streamlit as st
import random
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="PowerDice X-Cross", page_icon="⭐", layout="wide")

# ────────────────────────────────────────────────
# SESSION STATE
# ────────────────────────────────────────────────
if "player_names" not in st.session_state:
    st.session_state.player_names = None

if st.session_state.player_names is None:
    st.markdown("""
    <style>
        .welcome {
            background: linear-gradient(135deg, #0a0015, #200033);
            padding: 50px 20px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 0 50px #ff0066;
            margin: 20px;
        }
        .title {
            font-size: 60px;
            background: linear-gradient(90deg, #ff0066, #00ccff, #ffff00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome"><h1 class="title">POWER DICE X-CROSS</h1><p style="font-size:22px; color:#ffcc00;">Reach the center star first!</p></div>', unsafe_allow_html=True)

    st.markdown("### Enter player names (or keep defaults)", unsafe_allow_html=True)

    defaults = ["Player 1", "Player 2", "Player 3", "Player 4"]
    names_input = []
    cols = st.columns(4)

    for i, col in enumerate(cols):
        with col:
            name = st.text_input(f"Player {i+1}", value=defaults[i], key=f"init_{i}")
            names_input.append(name.strip() or defaults[i])

    if st.button("Start Game", type="primary", use_container_width=True):
        st.session_state.player_names = names_input
        st.session_state.positions = [1, 1, 1, 1]
        st.session_state.current_turn = 0
        st.session_state.round_num = 1
        st.session_state.winner = None
        st.rerun()

    st.stop()

# ────────────────────────────────────────────────
# GAME VARIABLES
# ────────────────────────────────────────────────
names   = st.session_state.player_names
emojis  = ["🔵", "🟠", "🟢", "🔴"]
colors  = ["#3399ff", "#ff8800", "#44cc77", "#ff3366"]

# ────────────────────────────────────────────────
# STYLES
# ────────────────────────────────────────────────
st.markdown("""
<style>
    .board {
        position: relative;
        width: 950px;
        height: 700px;
        margin: 30px auto;
        background: rgba(10,10,30,0.4);
        border-radius: 16px;
        border: 2px solid #444;
    }
    .arm {
        position: absolute;
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .row {
        display: flex;
        gap: 3px;
    }
    .cell {
        width: 42px;
        height: 42px;
        border-radius: 6px;
        border: 2px solid #222;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 13px;
        position: relative;
        box-shadow: 0 0 8px rgba(0,0,0,0.6);
    }
    .token {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        border: 2px solid #000;
        box-shadow: 0 0 12px currentColor;
        z-index: 10;
    }
    .star {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 90px;
        text-shadow: 0 0 20px #ffff66;
        z-index: 5;
    }
    .player-name {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 6px;
        white-space: nowrap;
    }
    .neon-title {
        font-size: 54px;
        background: linear-gradient(90deg, #ff3366, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0 0 20px #00ccff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="neon-title">POWER DICE X-CROSS ⭐</h1>', unsafe_allow_html=True)

# Winner screen
if st.session_state.winner:
    idx = names.index(st.session_state.winner)
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center; padding:40px; background:rgba(255,60,60,0.2); border:6px solid #ff4444; border-radius:20px;">
        <h1 style="font-size:70px; color:#ffdd00;">WINNER!</h1>
        <div style="font-size:90px; color:{colors[idx]};">
            {emojis[idx]} {st.session_state.winner} {emojis[idx]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Play Again – same players", type="primary"):
            st.session_state.positions = [1,1,1,1]
            st.session_state.current_turn = 0
            st.session_state.round_num = 1
            st.session_state.winner = None
            st.rerun()
    with c2:
        if st.button("New Players"):
            del st.session_state.player_names
            st.rerun()
    st.stop()

# Player status
cols = st.columns(4)
for i, col in enumerate(cols):
    with col:
        pos = st.session_state.positions[i]
        prog = min(pos / 16, 1)
        st.markdown(f"""
        <div style="padding:14px; border-radius:12px; text-align:center; border:3px solid {colors[i]}; background:rgba(20,20,50,0.7);">
            <h3 style="color:{colors[i]};">{emojis[i]} {names[i]}</h3>
            <div style="font-size:32px; color:#ffdd88;">{pos}</div>
            <div style="height:12px; background:#111; border-radius:6px; overflow:hidden; margin-top:6px;">
                <div style="height:100%; width:{prog*100}%; background:{colors[i]};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# X-CROSS BOARD – USING components.html
# ────────────────────────────────────────────────
st.markdown("### X-Cross Path to Center Star")

def create_arm(player_idx):
    pos = st.session_state.positions[player_idx]
    color = colors[player_idx]
    emoji = emojis[player_idx]
    name = names[player_idx]

    numbers = list(range(1, 16))
    row1 = numbers[:8]
    row2 = numbers[8:]

    cells_row1 = "".join(f'<div class="cell" style="background:{color}">{n}</div>' for n in row1)
    cells_row2 = "".join(f'<div class="cell" style="background:{color}">{n}</div>' for n in row2)

    token_html = ""
    if 1 <= pos <= 15:
        token_html = f'<div class="token" style="background:{color}">{emoji}</div>'

    top_pos = ["22%", "22%", "60%", "60%"][player_idx]
    left_pos = ["6%", "58%", "6%", "58%"][player_idx]
    angle = [-45, 45, -135, 135][player_idx]

    return f"""
    <div class="arm" style="top:{top_pos}; left:{left_pos}; transform:rotate({angle}deg);">
        <div class="player-name" style="color:{color}">{name}</div>
        <div class="row">{cells_row1}</div>
        <div class="row">{cells_row2}</div>
        {token_html}
    </div>
    """

center_tokens = ""
for i in range(4):
    if st.session_state.positions[i] == 16:
        center_tokens += f'<div class="token" style="background:{colors[i]}; width:40px; height:40px; font-size:26px; margin:4px;">{emojis[i]}</div>'

board_html = f"""
<div class="board">
    {create_arm(0)}
    {create_arm(1)}
    {create_arm(2)}
    {create_arm(3)}
    <div class="star">⭐</div>
    <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); display:flex; flex-wrap:wrap; gap:6px; width:180px; justify-content:center; z-index:10;">
        {center_tokens}
    </div>
</div>
"""

# This is the key line — using components.html instead of st.markdown
components.html(board_html, height=800, scrolling=False)

# ────────────────────────────────────────────────
# GAME CONTROLS
# ────────────────────────────────────────────────
curr = st.session_state.current_turn
curr_name = names[curr]

st.markdown(f"### Round {st.session_state.round_num}  –  Power: **{curr_name} {emojis[curr]}**")

if st.button(f"Roll Dice – {curr_name}", type="primary", use_container_width=True):
    placeholder = st.empty()

    for _ in range(8):
        v = random.choice([1,2,-1,-2])
        col = "#44ff88" if v > 0 else "#ff4444"
        sym = "⚀" if abs(v)==1 else "⚁"
        placeholder.markdown(f"""
        <div style="text-align:center; margin:30px;">
            <div style="width:130px;height:130px;margin:auto;background:#111133;border:8px solid #ddd;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:80px;color:{col};">
                {sym}
            </div>
            <div style="font-size:32px;color:{col};">{v:+d}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.11)

    roll = random.choice([1,2,-1,-2])
    col = "#44ff88" if roll > 0 else "#ff4444"
    sym = "⚀" if abs(roll)==1 else "⚁"
    placeholder.markdown(f"""
    <div style="text-align:center; margin:30px;">
        <div style="width:130px;height:130px;margin:auto;background:#111133;border:8px solid #ddd;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:80px;color:{col};">
            {sym}
        </div>
        <div style="font-size:36px;color:{col};">{roll:+d}</div>
    </div>
    """, unsafe_allow_html=True)

    # Apply base move
    for i in range(4):
        if st.session_state.positions[i] < 16:
            st.session_state.positions[i] += 1

    # Extra move for power player
    p = st.session_state.positions[curr]
    new_p = p + roll
    if 1 <= new_p <= 16:
        st.session_state.positions[curr] = new_p

    # Check winner
    for i in range(4):
        if st.session_state.positions[i] == 16:
            st.session_state.winner = names[i]
            break

    st.session_state.current_turn = (curr + 1) % 4
    st.session_state.round_num += 1
    st.rerun()

with st.expander("Rules"):
    st.markdown("""
- Each player has their own path (1–15) → center star (16)
- Every round **everyone** moves +1
- Power player rolls extra: +1 / +2 / -1 / -2
- First to exactly reach 16 wins
- Must land exactly (no overshooting)
    """)

st.caption("Using components.html • rotated arms • tokens centered in cells • 2025 edition")
