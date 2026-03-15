import streamlit as st
import random
import time

st.set_page_config(page_title="PowerDice X-Cross", page_icon="⭐", layout="wide")

# ────────────────────────────────────────────────
# SESSION STATE INIT
# ────────────────────────────────────────────────
if "player_names" not in st.session_state:
    st.session_state.player_names = None

if st.session_state.player_names is None:
    st.markdown("""
    <style>
        .welcome {background: linear-gradient(135deg, #0a0015, #1f0033); padding:60px; border-radius:25px; text-align:center; box-shadow:0 0 60px #ff3366;}
        .neon {font-size:64px; background:linear-gradient(90deg,#ff3366,#00ccff,#ffff66); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome"><h1 class="neon">POWER DICE X-CROSS</h1><p style="color:#ffcc33; font-size:22px;">Reach the center star first!</p></div>', unsafe_allow_html=True)

    cols = st.columns(4)
    defaults = ["Player 1", "Player 2", "Player 3", "Player 4"]
    names_input = []

    for i, col in enumerate(cols):
        with col:
            name = st.text_input(f"Player {i+1}", defaults[i], key=f"init_name_{i}")
            names_input.append(name.strip() or defaults[i])

    if st.button("START GAME", type="primary", use_container_width=True):
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
colors  = ["#3399ff", "#ff8800", "#44dd88", "#ff3366"]  # blue, orange, green, red

# ────────────────────────────────────────────────
# STYLES
# ────────────────────────────────────────────────
st.markdown("""
<style>
    .neon-title {font-size:54px; background:linear-gradient(90deg,#ff3366,#00ccff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-align:center; text-shadow:0 0 20px #00ccff;}
    .player-card {padding:14px; border-radius:14px; text-align:center; border:3px solid; margin:8px; background:rgba(20,20,50,0.7);}
    .cell {width:54px; height:54px; margin:2px; border:3px solid; border-radius:10px; background:#0a0a1f; color:#ffdd99; font-weight:bold; font-size:14px; display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:0 0 10px currentColor;}
    .tok {width:30px; height:30px; border-radius:50%; font-size:20px; box-shadow:0 0 12px currentColor; border:2px solid #000; display:flex; align-items:center; justify-content:center;}
    .star-center {width:140px; height:140px; background:radial-gradient(#ff4444, #880000); border-radius:50%; font-size:100px; color:white; display:flex; align-items:center; justify-content:center; box-shadow:0 0 60px #ff0000; animation:pulse 2.4s infinite;}
    @keyframes pulse {0%,100%{transform:scale(1);} 50%{transform:scale(1.08);}}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="neon-title">POWER DICE X-CROSS ⭐</h1>', unsafe_allow_html=True)

# ────────────────────────────────────────────────
# WIN SCREEN
# ────────────────────────────────────────────────
if st.session_state.winner:
    idx = names.index(st.session_state.winner)
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center; padding:50px; background:rgba(255,80,80,0.2); border:8px solid #ff4444; border-radius:25px;">
        <h1 style="font-size:80px; color:#ffff66;">WINNER!</h1>
        <div style="font-size:100px; color:{colors[idx]};">
            {emojis[idx]} {st.session_state.winner} {emojis[idx]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Play Again (same players)", type="primary"):
            st.session_state.positions = [1,1,1,1]
            st.session_state.current_turn = 0
            st.session_state.round_num = 1
            st.session_state.winner = None
            st.rerun()
    with c2:
        if st.button("Change Players"):
            del st.session_state.player_names
            st.rerun()
    st.stop()

# ────────────────────────────────────────────────
# PLAYER STATUS
# ────────────────────────────────────────────────
cols = st.columns(4)
for i, c in enumerate(cols):
    with c:
        pos = st.session_state.positions[i]
        prog = min(pos / 16.0, 1.0)
        st.markdown(f"""
        <div class="player-card" style="border-color:{colors[i]}; color:{colors[i]};">
            <h3>{emojis[i]} {names[i]}</h3>
            <div style="font-size:34px; color:#ffdd99;">{pos}</div>
            <div style="height:12px; background:#111; border-radius:6px; overflow:hidden; margin-top:6px;">
                <div style="height:100%; width:{prog*100}%; background:linear-gradient(90deg,#ffdd99,{colors[i]});"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# X-SHAPED GRID (17×17 virtual grid, only X positions used)
# ────────────────────────────────────────────────
st.markdown("### X-Cross Path to Center Star")

# Helper to render one cell
def render_cell(player_idx, number, is_center=False):
    pos = st.session_state.positions[player_idx]
    colr = colors[player_idx]
    has_token = (pos == number) and not is_center
    token_html = f'<div class="tok" style="background:{colr};">{emojis[player_idx]}</div>' if has_token else ''
    
    if is_center:
        tokens_html = ""
        for i in range(4):
            if st.session_state.positions[i] == 16:
                tokens_html += f'<div class="tok" style="background:{colors[i]}; width:42px; height:42px; font-size:26px; margin:4px;">{emojis[i]}</div>'
        st.markdown(f"""
        <div class="star-center" style="margin:20px auto; position:relative;">
            ⭐
            <div style="position:absolute; inset:0; display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:6px;">
                {tokens_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="cell" style="border-color:{colr};">
            {number}<br>{token_html}
        </div>
        """, unsafe_allow_html=True)

# Create 17×17 grid layout (only diagonal positions are used)
grid_size = 17
center = grid_size // 2   # 8

for row in range(grid_size):
    cols = st.columns(grid_size)
    
    for col_idx in range(grid_size):
        with cols[col_idx]:
            # Only render cells on the two diagonals
            if row == col_idx or row + col_idx == grid_size - 1:
                # Calculate logical position number along the diagonal
                if row < center:
                    # Top-left to bottom-right diagonal (one player)
                    num = row + 1
                    render_cell(0, num)
                elif row == center and col_idx == center:
                    # Center star
                    render_cell(-1, 16, is_center=True)
                elif row > center:
                    # Bottom-left to top-right diagonal (another player)
                    num = (grid_size - 1 - row) + 1
                    render_cell(2, num)
            else:
                # Empty cell to maintain grid spacing
                st.markdown("<div style='width:54px; height:54px; margin:2px;'></div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# CONTROLS
# ────────────────────────────────────────────────
turn = st.session_state.current_turn
curr_name = names[turn]

st.markdown(f"### Round {st.session_state.round_num} – Power Player: **{curr_name} {emojis[turn]}**")

if st.button(f"ROLL DICE – {curr_name}", type="primary", use_container_width=True):
    placeholder = st.empty()
    
    for _ in range(9):
        v = random.choice([1,2,-1,-2])
        c = "#66ff99" if v > 0 else "#ff4444"
        d = "⚀" if abs(v)==1 else "⚁"
        placeholder.markdown(f"""
        <div style="text-align:center; margin:30px;">
            <div style="width:130px;height:130px;margin:auto;background:#111133;border:10px solid #ccc;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:80px;color:{c};">
                {d}
            </div>
            <div style="font-size:32px;color:{c};">{v:+d}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)
    
    roll = random.choice([1,2,-1,-2])
    c = "#66ff99" if roll > 0 else "#ff4444"
    d = "⚀" if abs(roll)==1 else "⚁"
    placeholder.markdown(f"""
    <div style="text-align:center; margin:30px;">
        <div style="width:130px;height:130px;margin:auto;background:#111133;border:10px solid #ccc;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:80px;color:{c};">
            {d}
        </div>
        <div style="font-size:36px;color:{c};">{roll:+d}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Apply base +1 to everyone
    for i in range(4):
        if st.session_state.positions[i] < 16:
            st.session_state.positions[i] += 1
    
    # Extra move for current player
    p = st.session_state.positions[turn]
    newp = p + roll
    if 1 <= newp <= 16:
        st.session_state.positions[turn] = newp
    
    # Check win
    for i in range(4):
        if st.session_state.positions[i] == 16:
            st.session_state.winner = names[i]
            break
    
    st.session_state.current_turn = (turn + 1) % 4
    st.session_state.round_num += 1
    st.rerun()

with st.expander("Rules"):
    st.write("""
• Each player has their own path of 15 squares + center star (16)
• Every round: **all players** move +1
• Power player gets extra roll: +1 / +2 / -1 / -2
• First to exactly reach 16 wins
• Must land exactly (no overshooting)
    """)

st.caption("X-cross layout • separate paths per player • Karachi 2025 edition")
