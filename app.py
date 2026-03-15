import streamlit as st
import random
import time

st.set_page_config(page_title="PowerDice Ludo – Cross X ⭐", page_icon="⭐", layout="wide")

# ────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ────────────────────────────────────────────────
if "player_names" not in st.session_state:
    st.session_state.player_names = None

if st.session_state.player_names is None:
    # ────── WELCOME SCREEN ──────
    st.markdown("""
    <style>
        .welcome-bg {
            background: linear-gradient(135deg, #0d001a, #1a0033, #330033);
            padding: 60px 20px;
            border-radius: 25px;
            text-align: center;
            box-shadow: 0 0 60px #ff00cc, inset 0 0 30px #00ffcc;
            margin: 20px 0;
        }
        .neon-title {
            font-size: 64px;
            background: linear-gradient(90deg, #ff00cc, #00ffcc, #ffff00, #ff00cc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 300%;
            animation: gradient 6s ease infinite;
        }
        @keyframes gradient {0%{background-position:0%} 50%{background-position:100%} 100%{background-position:0%}}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome-bg"><h1 class="neon-title">POWERDICE LUDO<br>CROSS X ⭐</h1></div>', unsafe_allow_html=True)
    st.markdown("### Enter your players (like real mobile games)", unsafe_allow_html=True)

    cols = st.columns(4)
    default_names = ["Fahad", "Jawad", "Arslan", "Raza"]
    player_names_input = []

    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<h3 style='color:{['#ff3366','#3388ff','#33ff99','#ffee33'][i]};'>{['🔴','🔵','🟢','🟡'][i]} Player {i+1}</h3>", unsafe_allow_html=True)
            name = st.text_input("", value=default_names[i], key=f"init_name_{i}", label_visibility="collapsed")
            player_names_input.append(name.strip() if name.strip() else f"Player {i+1}")

    if st.button("🚀 START THE GAME", type="primary", use_container_width=True):
        st.session_state.player_names = player_names_input
        st.session_state.positions = [1, 1, 1, 1]
        st.session_state.current_index = 0
        st.session_state.round_num = 1
        st.session_state.winner = None
        st.session_state.last_roll = None
        st.rerun()

    st.stop()

# ────────────────────────────────────────────────
# GAME VARIABLES
# ────────────────────────────────────────────────
player_names = st.session_state.player_names
emojis       = ["🔴", "🔵", "🟢", "🟡"]
hex_colors   = ["#ff3366", "#3388ff", "#33ff99", "#ffee33"]

# ────────────────────────────────────────────────
# STYLES
# ────────────────────────────────────────────────
st.markdown("""
<style>
    .neon-title {font-size:56px; background:linear-gradient(90deg,#ff00cc,#00ffcc); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-align:center; text-shadow:0 0 30px #00ffcc;}
    .player-card {padding:16px; border-radius:16px; text-align:center; border:3px solid; margin:8px; background:linear-gradient(135deg,rgba(255,255,255,0.08),rgba(0,0,0,0.4));}
    .square {width:54px; height:54px; background:#0f0f1f; border:3px solid; border-radius:10px; display:flex; flex-direction:column; align-items:center; justify-content:center; font-size:13px; color:#ffd700; box-shadow:0 0 12px currentColor; margin:3px;}
    .token {width:30px; height:30px; border-radius:50%; font-size:20px; box-shadow:0 0 14px currentColor; border:2px solid #000; display:flex; align-items:center; justify-content:center;}
    .center-star {width:180px; height:180px; background:conic-gradient(#ffd700,#ff00cc,#00ffcc,#ffff00,#ffd700); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:140px; box-shadow:0 0 90px #ffff00, inset 0 0 50px #000; animation:pulse-star 3s infinite; position:relative;}
    @keyframes pulse-star {0%,100%{transform:scale(1);} 50%{transform:scale(1.1);}}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="neon-title">POWERDICE LUDO – CROSS X ⭐</h1>', unsafe_allow_html=True)

# ────────────────────────────────────────────────
# WINNER SCREEN
# ────────────────────────────────────────────────
if st.session_state.winner:
    win_idx = player_names.index(st.session_state.winner)
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center; padding:50px; background:rgba(255,215,0,0.15); border:8px solid #ffd700; border-radius:25px;">
        <h1 style="font-size:80px; color:#ffd700;">🏆 WINNER 🏆</h1>
        <h2 style="font-size:100px; color:{hex_colors[win_idx]};">
            {emojis[win_idx]} {st.session_state.winner} {emojis[win_idx]}
        </h2>
        <p style="font-size:28px;">Reached the CENTER STAR first!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again (same players)", type="primary"):
            st.session_state.positions = [1,1,1,1]
            st.session_state.current_index = 0
            st.session_state.round_num = 1
            st.session_state.winner = None
            st.rerun()
    with col2:
        if st.button("👥 Change Players"):
            del st.session_state.player_names
            st.rerun()
    st.stop()

# ────────────────────────────────────────────────
# PLAYER CARDS
# ────────────────────────────────────────────────
cols = st.columns(4)
for i, col in enumerate(cols):
    with col:
        pos = st.session_state.positions[i]
        progress = pos / 16
        st.markdown(f"""
        <div class="player-card" style="border-color:{hex_colors[i]}; color:{hex_colors[i]};">
            <h3>{emojis[i]} {player_names[i]}</h3>
            <div style="font-size:36px; color:#ffd700;">{pos}</div>
            <div style="height:14px; background:#222; border-radius:8px; overflow:hidden; margin-top:8px;">
                <div style="height:100%; width:{progress*100}%; background:linear-gradient(90deg,#ffd700,{hex_colors[i]});"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# BOARD – SEPARATE PATHS USING COLUMNS
# ────────────────────────────────────────────────
st.subheader("🌟 YOUR PATHS – CORNER → CENTER STAR 🌟")

def render_square(player_idx, pos_num):
    current_pos = st.session_state.positions[player_idx]
    color = hex_colors[player_idx]
    emoji = emojis[player_idx]
    has_token = (current_pos == pos_num)
    
    token_div = ""
    if has_token:
        token_div = f'<div class="token" style="background:{color};">{emoji}</div>'
    
    st.markdown(f"""
    <div class="square" style="border-color:{color};">
        <div>{pos_num}</div>
        {token_div}
    </div>
    """, unsafe_allow_html=True)

# TOP arm – Player 0
st.markdown(f'<h4 style="text-align:center; color:{hex_colors[0]};">🔴 {player_names[0]} – TOP PATH</h4>', unsafe_allow_html=True)
top_cols = st.columns(15)
for i, col in enumerate(top_cols):
    with col:
        render_square(0, i+1)

# MIDDLE – LEFT + CENTER + RIGHT
mid_cols = st.columns([1, 5, 3, 5, 1])

with mid_cols[0]:  # LEFT – Player 3
    st.markdown(f'<h4 style="text-align:center; color:{hex_colors[3]}; transform:rotate(-90deg); margin:80px 0;">🟡 {player_names[3]} – LEFT</h4>', unsafe_allow_html=True)
    left_cols = st.columns(1)
    for sq in range(1, 16):
        render_square(3, sq)

with mid_cols[2]:  # CENTER STAR
    star_tokens = ""
    for i in range(4):
        if st.session_state.positions[i] == 16:
            star_tokens += f'<div class="token" style="background:{hex_colors[i]}; width:48px; height:48px; font-size:32px; margin:4px;">{emojis[i]}</div>'
    
    st.markdown(f"""
    <div class="center-star">
        ⭐
        <div style="position:absolute; display:flex; flex-wrap:wrap; width:160px; justify-content:center; gap:8px;">
            {star_tokens}
        </div>
    </div>
    """, unsafe_allow_html=True)

with mid_cols[4]:  # RIGHT – Player 1
    st.markdown(f'<h4 style="text-align:center; color:{hex_colors[1]}; transform:rotate(90deg); margin:80px 0;">🔵 {player_names[1]} – RIGHT</h4>', unsafe_allow_html=True)
    for sq in range(1, 16):
        render_square(1, sq)

# BOTTOM arm – Player 2
st.markdown(f'<h4 style="text-align:center; color:{hex_colors[2]};">🟢 {player_names[2]} – BOTTOM PATH</h4>', unsafe_allow_html=True)
bottom_cols = st.columns(15)
for i, col in enumerate(bottom_cols):
    with col:
        render_square(2, i+1)

# ────────────────────────────────────────────────
# DICE & TURN
# ────────────────────────────────────────────────
current_idx = st.session_state.current_index
current_name = player_names[current_idx]

st.markdown(f"### ROUND {st.session_state.round_num} – POWER PLAYER: **{current_name} {emojis[current_idx]}**")

if st.button(f"🎲 ROLL POWER DICE – {current_name}", type="primary", use_container_width=True):
    placeholder = st.empty()
    
    # Rolling animation
    for _ in range(10):
        fake_val = random.choice([1, 2, -1, -2])
        color = "#33ff99" if fake_val > 0 else "#ff3366"
        dots = "⚀" if abs(fake_val) == 1 else "⚁"
        placeholder.markdown(f"""
        <div style="text-align:center; margin:30px 0;">
            <div style="width:140px; height:140px; margin:auto; background:#1a1a2e; border:10px solid #fff; border-radius:24px; 
                        display:flex; align-items:center; justify-content:center; font-size:90px; color:{color}; 
                        box-shadow:0 0 50px {color}; animation:spin 0.4s;">
                {dots}
            </div>
            <h2 style="color:{color};">{fake_val:+d}</h2>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.09)
    
    # Final roll
    roll = random.choice([1, 2, -1, -2])
    color = "#33ff99" if roll > 0 else "#ff3366"
    dots = "⚀" if abs(roll) == 1 else "⚁"
    placeholder.markdown(f"""
    <div style="text-align:center; margin:30px 0;">
        <div style="width:140px; height:140px; margin:auto; background:#1a1a2e; border:10px solid #fff; border-radius:24px; 
                    display:flex; align-items:center; justify-content:center; font-size:90px; color:{color}; box-shadow:0 0 60px #ffd700;">
            {dots}
        </div>
        <h2 style="color:{color};">{roll:+d} {'🟢' * abs(roll) if roll > 0 else '🔴' * abs(roll)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.last_roll = roll
    
    # Apply moves
    for i in range(4):
        if st.session_state.positions[i] < 16:
            st.session_state.positions[i] += 1
    
    # Power player extra move
    p_pos = st.session_state.positions[current_idx]
    new_pos = p_pos + roll
    if 1 <= new_pos <= 16:
        st.session_state.positions[current_idx] = new_pos
    
    # Check winner
    for i in range(4):
        if st.session_state.positions[i] == 16:
            st.session_state.winner = player_names[i]
            break
    
    st.session_state.current_index = (current_idx + 1) % 4
    st.session_state.round_num += 1
    st.rerun()

if st.session_state.last_roll is not None:
    r = st.session_state.last_roll
    c = "#33ff99" if r > 0 else "#ff3366"
    st.markdown(f"**Last roll:** <span style='color:{c}; font-size:28px;'>{ '⚀' if abs(r)==1 else '⚁' } {r:+d}</span>", unsafe_allow_html=True)

with st.expander("📜 Rules"):
    st.write("""
    • Each player has their own path from corner to CENTER STAR (position 16)
    • Every round: ALL players move +1 on their path
    • Power player rolls special dice: +1 / +2 (green) or -1 / -2 (red)
    • Extra move only for power player (if stays within 1–16)
    • First to **exactly** reach the CENTER STAR wins
    • Names can be changed by restarting
    """)

st.caption("Made for Fahad • Karachi vibes • Cross paths + real dice roll • Streamlit Cloud ready")
