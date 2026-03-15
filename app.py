import streamlit as st
import random
import time

st.set_page_config(page_title="PowerDice Cross Game", page_icon="⭐", layout="wide")

# ────────────────────────────────────────────────
# SESSION STATE
# ────────────────────────────────────────────────
if "player_names" not in st.session_state:
    st.session_state.player_names = None

if st.session_state.player_names is None:
    # Welcome screen
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

    st.markdown('<div class="welcome"><h1 class="title">POWER DICE CROSS</h1><p style="font-size:22px; color:#ffcc00;">Reach the center star first!</p></div>', unsafe_allow_html=True)

    st.markdown("### Enter player names (or keep defaults)", unsafe_allow_html=True)

    defaults = ["Player 1", "Player 2", "Player 3", "Player 4"]
    names = []
    cols = st.columns(4)

    for i, col in enumerate(cols):
        with col:
            name = st.text_input(f"Player {i+1}", value=defaults[i], key=f"init_{i}")
            names.append(name.strip() or defaults[i])

    if st.button("Start Game", type="primary", use_container_width=True):
        st.session_state.player_names = names
        st.session_state.positions = [1, 1, 1, 1]          # 1..15 = path, 16 = center
        st.session_state.current_turn = 0
        st.session_state.round_num = 1
        st.session_state.winner = None
        st.rerun()

    st.stop()

# ────────────────────────────────────────────────
# GAME DATA
# ────────────────────────────────────────────────
names   = st.session_state.player_names
emojis  = ["🔵", "🟠", "🟢", "🔴"]
colors  = ["#3399ff", "#ff8800", "#44cc77", "#ff3366"]   # blue, orange, green, red
arms    = ["TOP", "RIGHT", "BOTTOM", "LEFT"]

# ────────────────────────────────────────────────
# STYLES
# ────────────────────────────────────────────────
st.markdown("""
<style>
    .title {font-size:52px; background:linear-gradient(90deg,#ff0066,#00ccff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-align:center;}
    .player-box {
        padding:14px; border-radius:12px; text-align:center; margin:6px;
        border:3px solid; background:linear-gradient(135deg,rgba(30,30,50,0.7),rgba(10,10,30,0.9));
    }
    .sq {
        width:50px; height:50px; margin:3px; border:3px solid; border-radius:8px;
        background:#0d0d1f; color:#ffdd88; font-weight:bold; font-size:13px;
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        box-shadow:0 0 10px currentColor;
    }
    .token {
        width:28px; height:28px; border-radius:50%; font-size:18px;
        box-shadow:0 0 12px currentColor; border:2px solid #000;
        display:flex; align-items:center; justify-content:center;
    }
    .big-star {
        width:160px; height:160px; font-size:120px; line-height:160px;
        background:radial-gradient(circle at 30% 30%, #ff4444, #aa0000);
        border-radius:50%; color:white; text-shadow:0 0 30px #ff0000;
        box-shadow:0 0 70px #ff0000, inset 0 0 30px #880000;
        animation: pulse 2.2s infinite;
    }
    @keyframes pulse {0%,100%{transform:scale(1);} 50%{transform:scale(1.12);}}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">POWER DICE CROSS ⭐</h1>', unsafe_allow_html=True)

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
        <p style="font-size:24px; color:#ffcc66;">Reached the center star first</p>
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
        <div class="player-box" style="border-color:{colors[i]}; color:{colors[i]};">
            <h3>{emojis[i]} {names[i]}</h3>
            <div style="font-size:32px; color:#ffdd88;">{pos}</div>
            <div style="height:12px; background:#222; border-radius:6px; overflow:hidden; margin-top:6px;">
                <div style="height:100%; width:{prog*100}%; background:{colors[i]};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# CROSS BOARD
# ────────────────────────────────────────────────
st.markdown("### Path to the Center Star")

def square(player_i, num):
    pos = st.session_state.positions[player_i]
    color = colors[player_i]
    tok = f'<div class="token" style="background:{color};">{emojis[player_i]}</div>' if pos == num else ''
    st.markdown(f"""
    <div class="sq" style="border-color:{color}">
        {num}<br>{tok}
    </div>
    """, unsafe_allow_html=True)

# TOP arm – Player 1 (blue)
st.markdown(f'<h4 style="text-align:center; color:{colors[0]};">↑ {names[0]} (blue)</h4>', unsafe_allow_html=True)
cols_top = st.columns(15)
for i, c in enumerate(cols_top):
    with c:
        square(0, i+1)

# Middle row: LEFT + STAR + RIGHT
mid = st.columns([1, 5, 3, 5, 1])

with mid[0]:  # LEFT – Player 4 (red)
    st.markdown(f'<h4 style="color:{colors[3]}; transform:rotate(-90deg); margin:100px 0;">← {names[3]} (red)</h4>', unsafe_allow_html=True)
    for n in range(1,16):
        square(3, n)

with mid[2]:  # CENTER STAR
    tokens_in_center = ""
    for i in range(4):
        if st.session_state.positions[i] == 16:
            tokens_in_center += f'<div class="token" style="background:{colors[i]}; width:44px; height:44px; font-size:28px; margin:4px;">{emojis[i]}</div>'

    st.markdown(f"""
    <div class="big-star" style="margin:30px auto; position:relative;">
        ⭐
        <div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:6px;">
            {tokens_in_center}
        </div>
    </div>
    """, unsafe_allow_html=True)

with mid[4]:  # RIGHT – Player 2 (orange)
    st.markdown(f'<h4 style="color:{colors[1]}; transform:rotate(90deg); margin:100px 0;">→ {names[1]} (orange)</h4>', unsafe_allow_html=True)
    for n in range(1,16):
        square(1, n)

# BOTTOM arm – Player 3 (green)
st.markdown(f'<h4 style="text-align:center; color:{colors[2]};">↓ {names[2]} (green)</h4>', unsafe_allow_html=True)
cols_bot = st.columns(15)
for i, c in enumerate(cols_bot):
    with c:
        square(2, i+1)

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
            <div style="width:130px;height:130px;margin:auto;background:#111133;border:8px solid #ddd;border-radius:20px;
                        display:flex;align-items:center;justify-content:center;font-size:80px;color:{col};">
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
        <div style="width:130px;height:130px;margin:auto;background:#111133;border:8px solid #ddd;border-radius:20px;
                    display:flex;align-items:center;justify-content:center;font-size:80px;color:{col};">
            {sym}
        </div>
        <div style="font-size:36px;color:{col};">{roll:+d}</div>
    </div>
    """, unsafe_allow_html=True)

    # Apply moves
    for i in range(4):
        if st.session_state.positions[i] < 16:
            st.session_state.positions[i] += 1

    # Power player extra
    p = st.session_state.positions[curr]
    new_p = p + roll
    if 1 <= new_p <= 16:
        st.session_state.positions[curr] = new_p

    # Winner check
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
- Current power player rolls extra: **+1**, **+2**, **-1** or **-2**
- First to **exactly** reach the star wins
- Must land exactly on 16 (no overshooting)
    """)

st.caption("Karachi 2025 • Simple cross version • Enjoy!")
