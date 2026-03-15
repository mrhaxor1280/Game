import streamlit as st
import random
import time

st.set_page_config(page_title="PowerDice Ludo ★ Cross X Edition", page_icon="🎲", layout="wide")

# ====================== SESSION STATE ======================
if "player_names" not in st.session_state:
    st.session_state.player_names = ["Fahad", "Jawad", "Arslan", "Raza"]

if "positions" not in st.session_state:
    st.session_state.positions = [1, 1, 1, 1]          # index 0 = player 0, etc.
    st.session_state.current_index = 0
    st.session_state.round_num = 1
    st.session_state.winner = None
    st.session_state.last_roll = None
    st.session_state.rolling = False

player_names = st.session_state.player_names
emojis = ["🔴", "🔵", "🟢", "🟡"]
hex_colors = ["#ff3366", "#3388ff", "#33ff99", "#ffee33"]

# ====================== SIDEBAR - CUSTOM NAMES ======================
with st.sidebar:
    st.header("👥 Customize Players")
    st.caption("Change names anytime (game resets positions)")
    new_names = []
    for i in range(4):
        name = st.text_input(f"Player {i+1}", value=player_names[i], key=f"name_input_{i}")
        new_names.append(name.strip() if name.strip() else f"Player {i+1}")
    
    if st.button("💾 Save Names & Reset Game", type="primary"):
        st.session_state.player_names = new_names
        st.session_state.positions = [1, 1, 1, 1]
        st.session_state.current_index = 0
        st.session_state.round_num = 1
        st.session_state.winner = None
        st.session_state.last_roll = None
        st.rerun()

# ====================== TITLE & RULES ======================
st.markdown("""
<style>
    .big-title {font-size: 68px; background: linear-gradient(90deg, #ff00cc, #00ffcc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; text-shadow: 0 0 30px #00ffcc;}
    .cross-board {background: #111; border: 12px solid #ffd700; border-radius: 30px; padding: 25px; box-shadow: 0 0 50px #ffd700, inset 0 0 40px #00ffcc;}
    .square {width: 68px; height: 68px; background: #222; border: 5px solid #ffd700; border-radius: 14px; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 13px; box-shadow: 0 0 18px #ffd700; transition: all 0.3s;}
    .token {width: 30px; height: 30px; border-radius: 50%; font-size: 20px; box-shadow: 0 0 10px currentColor; border: 3px solid #111;}
    .dice-real {width: 130px; height: 130px; background: #1a1a2e; border: 10px solid #fff; border-radius: 25px; display: flex; align-items: center; justify-content: center; font-size: 85px; box-shadow: 0 0 40px #fff, 0 0 60px #00ffcc; animation: roll-real 0.4s ease;}
    @keyframes roll-real {0%{transform:rotate(0deg) scale(0.7);} 50%{transform:rotate(360deg) scale(1.25);} 100%{transform:rotate(720deg) scale(1);}}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="big-title">POWERDICE LUDO<br><span style="font-size:32px;">CROSS X EDITION</span></h1>', unsafe_allow_html=True)
st.caption("Ludo King style • Cross-shaped track • Real rolling dice with dots • Custom players")

if st.session_state.winner:
    st.balloons()
    win_idx = player_names.index(st.session_state.winner)
    st.markdown(f"""
    <div style="text-align:center; padding:40px; background:rgba(0,255,204,0.2); border:8px solid #00ffcc; border-radius:25px;">
        <h1 style="font-size:80px;">🏆 WINNER 🏆</h1>
        <h2 style="font-size:90px; color:{hex_colors[win_idx]};">{emojis[win_idx]} {st.session_state.winner} {emojis[win_idx]}</h2>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 NEW GAME WITH SAME NAMES", type="primary"):
        st.session_state.positions = [1, 1, 1, 1]
        st.session_state.current_index = 0
        st.session_state.round_num = 1
        st.session_state.winner = None
        st.session_state.last_roll = None
        st.rerun()
else:
    # ====================== PLAYER PANELS (around the board) ======================
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            pos = st.session_state.positions[i]
            st.subheader(f"{emojis[i]} {player_names[i]}")
            st.progress(pos / 16)
            st.metric("Position", pos, label_visibility="collapsed")

    # ====================== CROSS X SHAPE TRACK ======================
    st.subheader("🎮 CROSS X TRACK (1 → 16)")
    st.markdown('<div class="cross-board">', unsafe_allow_html=True)
    
    # We build a visual CROSS using 5 rows with strategic columns
    # Top arm (positions 9-12)
    top_cols = st.columns([1,1,1,1,1,1,1])
    for i in range(4):
        with top_cols[i+1]:
            pos_num = 9 + i
            tokens_html = ""
            for j in range(4):
                if st.session_state.positions[j] == pos_num:
                    tokens_html += f'<span class="token" style="background:{hex_colors[j]};">{emojis[j]}</span>'
            st.markdown(f"""
            <div class="square" style="margin:8px auto;">
                <div style="color:#ffd700;font-weight:bold;">{pos_num}</div>
                <div style="display:flex;gap:3px;flex-wrap:wrap;justify-content:center;">{tokens_html}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Middle row - Left arm + Center + Right arm (positions 13-16 left, 5-8 right)
    mid_cols = st.columns([1, 2, 1, 2, 1])
    # Left arm (13-16)
    with mid_cols[0]:
        for p in [13,14,15,16]:
            tokens_html = ""
            for j in range(4):
                if st.session_state.positions[j] == p:
                    tokens_html += f'<span class="token" style="background:{hex_colors[j]};">{emojis[j]}</span>'
            st.markdown(f"""
            <div class="square" style="margin:5px;">
                <div style="color:#ffd700;font-weight:bold;">{p}</div>
                <div style="display:flex;gap:3px;flex-wrap:wrap;justify-content:center;">{tokens_html}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Center (positions 1-4 + 5-8 in cross middle - we show 1-4 here for visual flow)
    with mid_cols[2]:
        st.markdown('<div style="height:280px; display:flex; flex-direction:column; justify-content:center; gap:8px;">', unsafe_allow_html=True)
        for p in [1,2,3,4]:
            tokens_html = ""
            for j in range(4):
                if st.session_state.positions[j] == p:
                    tokens_html += f'<span class="token" style="background:{hex_colors[j]};">{emojis[j]}</span>'
            st.markdown(f"""
            <div class="square">
                <div style="color:#ffd700;font-weight:bold;">{p}</div>
                <div style="display:flex;gap:3px;flex-wrap:wrap;justify-content:center;">{tokens_html}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right arm (5-8)
    with mid_cols[4]:
        for p in [5,6,7,8]:
            tokens_html = ""
            for j in range(4):
                if st.session_state.positions[j] == p:
                    tokens_html += f'<span class="token" style="background:{hex_colors[j]};">{emojis[j]}</span>'
            st.markdown(f"""
            <div class="square" style="margin:5px;">
                <div style="color:#ffd700;font-weight:bold;">{p}</div>
                <div style="display:flex;gap:3px;flex-wrap:wrap;justify-content:center;">{tokens_html}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption("🔄 The path flows in CROSS shape exactly like Ludo King (top → right → bottom → left)")

    # ====================== POWER + REAL ROLLING DICE ======================
    current_idx = st.session_state.current_index
    current_name = player_names[current_idx]
    
    st.markdown(f"### 🔥 ROUND {st.session_state.round_num} — POWER PLAYER: **{current_name} {emojis[current_idx]}**")

    if st.button(f"🎲 ROLL SPECIAL DICE (Power: {current_name})", type="primary", use_container_width=True):
        # Real rolling animation with dots
        roll_value = random.choice([1, 2, -1, -2])
        
        placeholder = st.empty()
        
        # 8 frames of real dice motion
        for _ in range(8):
            fake_roll = random.choice([1, 2, -1, -2])
            fake_abs = abs(fake_roll)
            fake_color = "#33ff99" if fake_roll > 0 else "#ff3366"
            fake_symbol = "⚀" if fake_abs == 1 else "⚁"
            fake_sign = "+" if fake_roll > 0 else ""
            
            placeholder.markdown(f"""
            <div style="text-align:center;">
                <div class="dice-real" style="color:{fake_color};">
                    {fake_symbol}
                </div>
                <h3 style="color:{fake_color}; margin-top:10px;">{fake_sign}{fake_roll}</h3>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.12)
        
        # Final result
        abs_val = abs(roll_value)
        color = "#33ff99" if roll_value > 0 else "#ff3366"
        symbol = "⚀" if abs_val == 1 else "⚁"
        sign = "+" if roll_value > 0 else ""
        
        placeholder.markdown(f"""
        <div style="text-align:center;">
            <div class="dice-real" style="color:{color}; animation: none;">
                {symbol}
            </div>
            <h2 style="color:{color}; margin:15px 0;">{sign}{roll_value} { '🟢' if roll_value > 0 else '🔴' } × {abs_val}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.last_roll = roll_value
        
        # ====================== APPLY MOVES (exact rules) ======================
        # Base +1 to EVERYONE
        for i in range(4):
            if st.session_state.positions[i] < 16:
                st.session_state.positions[i] += 1
        
        # Extra move ONLY for power player
        after_base = st.session_state.positions[current_idx]
        if after_base + roll_value <= 16:
            st.session_state.positions[current_idx] += roll_value
        
        # Clamp
        for i in range(4):
            if st.session_state.positions[i] < 1:
                st.session_state.positions[i] = 1
            if st.session_state.positions[i] > 16:
                st.session_state.positions[i] = 16
        
        # Check winner
        for i in range(4):
            if st.session_state.positions[i] == 16:
                st.session_state.winner = player_names[i]
                break
        
        # Next power player
        st.session_state.current_index = (st.session_state.current_index + 1) % 4
        st.session_state.round_num += 1
        st.rerun()

    # Last roll recap
    if st.session_state.last_roll is not None:
        last = st.session_state.last_roll
        c = "#33ff99" if last > 0 else "#ff3366"
        s = "⚀" if abs(last) == 1 else "⚁"
        st.markdown(f"**Last roll:** <span style='color:{c}; font-size:28px;'>{s} {last:+d}</span>", unsafe_allow_html=True)

# ====================== HOW TO PLAY ======================
with st.expander("📜 Exact Rules (your original + new features)"):
    st.write("""
    • Everyone starts at 1  
    • Every round: **+1 base move** for ALL players  
    • Power player rolls special dice: **+1 / +2 (green)** or **-1 / -2 (red)**  
    • Exact landing on 16 required to win  
    • Turn order cycles automatically  
    • Full Ludo King cross X track + real rolling dice with dots  
    • Change player names anytime
    """)

st.caption("Built for Fahad • Cross X layout + real dice motion • Deployed on Streamlit Cloud in 1 click")
