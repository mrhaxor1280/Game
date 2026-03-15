import streamlit as st
import random
import time

st.set_page_config(page_title="PowerDice Ludo ★ Cross X", page_icon="⭐", layout="wide")

# ====================== SESSION STATE ======================
if "player_names" not in st.session_state:
    st.session_state.player_names = None

if st.session_state.player_names is None:
    # ====================== BEAUTIFUL WELCOME SCREEN (like real apps) ======================
    st.markdown("""
    <style>
        .welcome {background: linear-gradient(135deg, #0f0f23, #1a0033); padding: 60px; border-radius: 30px; text-align: center; box-shadow: 0 0 80px #ff00cc;}
        .neon-text {font-size: 72px; background: linear-gradient(90deg, #ff00cc, #00ffcc, #ffff00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 40px #00ffcc;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome"><h1 class="neon-text">POWERDICE LUDO</h1><h2 style="color:#00ffcc; font-size:32px;">CROSS X EDITION ⭐</h2><p style="font-size:22px; color:#ffd700;">Each player has their own neon path from corner to CENTER STAR!</p></div>', unsafe_allow_html=True)

    st.markdown("### 👥 Enter Player Names (exactly like real mobile games)")
    cols = st.columns(4)
    names = []
    default_names = ["Fahad", "Jawad", "Arslan", "Raza"]
    emojis = ["🔴", "🔵", "🟢", "🟡"]
    colors = ["#ff3366", "#3388ff", "#33ff99", "#ffee33"]

    for i in range(4):
        with cols[i]:
            st.markdown(f'<h3 style="color:{colors[i]};">{emojis[i]} Player {i+1}</h3>', unsafe_allow_html=True)
            name = st.text_input("Name", value=default_names[i], key=f"init_{i}", label_visibility="collapsed")
            names.append(name.strip() if name.strip() else f"Player {i+1}")

    if st.button("🚀 START GAME NOW", type="primary", use_container_width=True):
        st.session_state.player_names = names
        st.session_state.positions = [1, 1, 1, 1]      # each player starts at 1 (corner)
        st.session_state.current_index = 0
        st.session_state.round_num = 1
        st.session_state.winner = None
        st.session_state.last_roll = None
        st.rerun()

    st.caption("Each player moves on their own colorful path from corner → center ⭐ | First to reach the star wins!")
    st.stop()

# ====================== MAIN GAME (after names entered) ======================
player_names = st.session_state.player_names
emojis = ["🔴", "🔵", "🟢", "🟡"]
hex_colors = ["#ff3366", "#3388ff", "#33ff99", "#ffee33"]
arm_names = ["TOP (Red)", "RIGHT (Blue)", "BOTTOM (Green)", "LEFT (Yellow)"]

st.markdown("""
<style>
    .neon-title {font-size: 58px; background: linear-gradient(90deg, #ff00cc, #00ffcc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; text-shadow: 0 0 50px #00ffcc;}
    .board {background: #0a0a1f; border: 14px solid #ffd700; border-radius: 40px; padding: 30px; box-shadow: 0 0 80px #ffd700, inset 0 0 60px #00ffcc; max-width: 1100px; margin: 20px auto;}
    .arm {background: rgba(255,255,255,0.05); border-radius: 20px; padding: 12px; box-shadow: 0 0 30px currentColor;}
    .top-arm, .bottom-arm {display: flex; gap: 6px; justify-content: center;}
    .left-arm, .right-arm {display: flex; flex-direction: column; gap: 6px; justify-content: center;}
    .square {width: 42px; height: 42px; background: #111; border: 4px solid; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold; color: #ffd700; box-shadow: 0 0 15px #ffd700; transition: all 0.3s;}
    .token {width: 28px; height: 28px; border-radius: 50%; font-size: 18px; box-shadow: 0 0 15px currentColor; border: 3px solid #111;}
    .center-star {width: 140px; height: 140px; background: linear-gradient(#ffd700, #ff00cc); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 110px; box-shadow: 0 0 80px #ffff00, 0 0 120px #ff00cc; animation: pulse 2s infinite;}
    @keyframes pulse {0%,100%{transform:scale(1);} 50%{transform:scale(1.12);}}
    .arm-label {text-align:center; font-size:18px; font-weight:bold; margin-bottom:8px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="neon-title">POWERDICE LUDO<br>CROSS X ⭐</h1>', unsafe_allow_html=True)
st.markdown(f"**Playing with:** {emojis[0]} {player_names[0]} • {emojis[1]} {player_names[1]} • {emojis[2]} {player_names[2]} • {emojis[3]} {player_names[3]}", unsafe_allow_html=True)

if st.session_state.winner:
    win_idx = player_names.index(st.session_state.winner)
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center; padding:50px; background:rgba(255,215,0,0.2); border:10px solid #ffd700; border-radius:30px;">
        <h1 style="font-size:90px;">🏆 WINNER 🏆</h1>
        <h2 style="font-size:110px; color:{hex_colors[win_idx]};">{emojis[win_idx]} {st.session_state.winner} {emojis[win_idx]}</h2>
        <p style="font-size:28px;">Reached the CENTER STAR first!</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Restart Same Players", type="primary", use_container_width=True):
            st.session_state.positions = [1, 1, 1, 1]
            st.session_state.current_index = 0
            st.session_state.round_num = 1
            st.session_state.winner = None
            st.session_state.last_roll = None
            st.rerun()
    with col2:
        if st.button("👥 New Players", use_container_width=True):
            del st.session_state.player_names
            st.rerun()
    st.stop()

# ====================== COLORFUL PLAYER PANELS ======================
cols = st.columns(4)
for i in range(4):
    pos = st.session_state.positions[i]
    progress = min(pos / 16 * 100, 100)
    with cols[i]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {hex_colors[i]}, #111); padding:15px; border-radius:20px; text-align:center; border:4px solid {hex_colors[i]};">
            <h3>{emojis[i]} {player_names[i]}</h3>
            <div style="font-size:48px; color:#ffd700;">{pos}</div>
            <div style="height:18px; background:#222; border-radius:10px; overflow:hidden;">
                <div style="height:100%; width:{progress}%; background:linear-gradient(#ffd700, {hex_colors[i]});"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ====================== SUPER COLORFUL CROSS X BOARD (separate paths) ======================
st.subheader("🌟 YOUR PATHS FROM CORNERS TO CENTER STAR 🌟")

board_html = '<div class="board">'

# TOP ARM - Player 0 (Red)
board_html += f'<div class="arm-label" style="color:{hex_colors[0]};">🔴 {player_names[0]} TOP PATH</div>'
board_html += '<div class="top-arm">'
for sq in range(1, 16):
    token_html = ""
    if st.session_state.positions[0] == sq:
        token_html = f'<span class="token" style="background:{hex_colors[0]};">{emojis[0]}</span>'
    board_html += f"""
    <div class="square" style="border-color:{hex_colors[0]};">
        <div style="font-size:11px;">{sq}</div>
        {token_html}
    </div>
    """
board_html += '</div>'

# MIDDLE ROW
board_html += '<div style="display:flex; align-items:center; gap:30px; justify-content:center; margin:20px 0;">'

# LEFT ARM - Player 3 (Yellow)
board_html += f'<div><div class="arm-label" style="color:{hex_colors[3]};">🟡 {player_names[3]} LEFT PATH</div><div class="left-arm">'
for sq in range(1, 16):
    token_html = ""
    if st.session_state.positions[3] == sq:
        token_html = f'<span class="token" style="background:{hex_colors[3]};">{emojis[3]}</span>'
    board_html += f"""
    <div class="square" style="border-color:{hex_colors[3]};">
        <div style="font-size:11px;">{sq}</div>
        {token_html}
    </div>
    """
board_html += '</div></div>'

# CENTER STAR
center_tokens = ""
for i in range(4):
    if st.session_state.positions[i] == 16:
        center_tokens += f'<span class="token" style="background:{hex_colors[i]}; width:48px; height:48px; font-size:32px;">{emojis[i]}</span>'
board_html += f"""
<div class="center-star" style="border:8px solid #ffd700;">
    ⭐
    <div style="position:absolute; margin-top:70px; display:flex; gap:8px;">{center_tokens}</div>
</div>
"""

# RIGHT ARM - Player 1 (Blue)
board_html += f'<div><div class="arm-label" style="color:{hex_colors[1]};">🔵 {player_names[1]} RIGHT PATH</div><div class="right-arm">'
for sq in range(1, 16):
    token_html = ""
    if st.session_state.positions[1] == sq:
        token_html = f'<span class="token" style="background:{hex_colors[1]};">{emojis[1]}</span>'
    board_html += f"""
    <div class="square" style="border-color:{hex_colors[1]};">
        <div style="font-size:11px;">{sq}</div>
        {token_html}
    </div>
    """
board_html += '</div></div>'

board_html += '</div>'   # end middle

# BOTTOM ARM - Player 2 (Green)
board_html += f'<div class="arm-label" style="color:{hex_colors[2]};">🟢 {player_names[2]} BOTTOM PATH</div>'
board_html += '<div class="bottom-arm">'
for sq in range(1, 16):
    token_html = ""
    if st.session_state.positions[2] == sq:
        token_html = f'<span class="token" style="background:{hex_colors[2]};">{emojis[2]}</span>'
    board_html += f"""
    <div class="square" style="border-color:{hex_colors[2]};">
        <div style="font-size:11px;">{sq}</div>
        {token_html}
    </div>
    """
board_html += '</div>'

board_html += '</div>'   # end board

st.markdown(board_html, unsafe_allow_html=True)

# ====================== POWER & REAL ROLLING DICE ======================
current_idx = st.session_state.current_index
current_name = player_names[current_idx]

st.markdown(f"### 🔥 ROUND {st.session_state.round_num} — POWER PLAYER: **{current_name} {emojis[current_idx]}**")

if st.button(f"🎲 ROLL SPECIAL DICE (Power: {current_name})", type="primary", use_container_width=True):
    roll_value = random.choice([1, 2, -1, -2])
    
    placeholder = st.empty()
    for _ in range(9):
        fake = random.choice([1, 2, -1, -2])
        fake_color = "#33ff99" if fake > 0 else "#ff3366"
        fake_symbol = "⚀" if abs(fake) == 1 else "⚁"
        placeholder.markdown(f"""
        <div style="text-align:center; margin:30px;">
            <div style="width:150px; height:150px; margin:auto; background:#1a1a2e; border:12px solid #fff; border-radius:30px; display:flex; align-items:center; justify-content:center; font-size:92px; color:{fake_color}; box-shadow:0 0 60px #00ffcc; animation:roll-real 0.35s;">
                {fake_symbol}
            </div>
            <h2 style="color:{fake_color};">{fake:+d}</h2>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.09)
    
    # Final result
    color = "#33ff99" if roll_value > 0 else "#ff3366"
    symbol = "⚀" if abs(roll_value) == 1 else "⚁"
    placeholder.markdown(f"""
    <div style="text-align:center; margin:30px;">
        <div style="width:150px; height:150px; margin:auto; background:#1a1a2e; border:12px solid #fff; border-radius:30px; display:flex; align-items:center; justify-content:center; font-size:92px; color:{color}; box-shadow:0 0 80px #ffd700;">
            {symbol}
        </div>
        <h2 style="color:{color}; font-size:42px;">{roll_value:+d} {'🟢' if roll_value > 0 else '🔴'}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.last_roll = roll_value
    
    # === APPLY MOVES (each on their own path) ===
    for i in range(4):
        if st.session_state.positions[i] < 16:
            st.session_state.positions[i] += 1
    
    # Extra move for power player only
    after = st.session_state.positions[current_idx]
    if after + roll_value <= 16 and after + roll_value >= 1:
        st.session_state.positions[current_idx] += roll_value
    
    # Clamp
    for i in range(4):
        if st.session_state.positions[i] < 1:
            st.session_state.positions[i] = 1
    
    # Check winner
    for i in range(4):
        if st.session_state.positions[i] == 16:
            st.session_state.winner = player_names[i]
            break
    
    st.session_state.current_index = (st.session_state.current_index + 1) % 4
    st.session_state.round_num += 1
    st.rerun()

if st.session_state.last_roll is not None:
    last = st.session_state.last_roll
    c = "#33ff99" if last > 0 else "#ff3366"
    st.markdown(f"**Last roll:** <span style='color:{c}; font-size:32px;'>{'⚀' if abs(last)==1 else '⚁'} {last:+d}</span>", unsafe_allow_html=True)

with st.expander("📜 How to Play (your exact rules)"):
    st.write("""
    • Each player has their OWN colorful path from corner to CENTER ⭐  
    • Every round: +1 move for ALL players on their own path  
    • Power player rolls special dice: +1 / +2 (green) or -1 / -2 (red)  
    • First to reach exactly the CENTER STAR (16) WINS!  
    • Exact landing required • Turn order cycles  
    """)

st.caption("Built with love for Fahad • Separate neon paths + real rolling dice + center star • Fully deployed on Streamlit Cloud")
