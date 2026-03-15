import streamlit as st
import random
import time

st.set_page_config(page_title="PowerDice Ludo", page_icon="🎲", layout="wide")

# Session state
if "positions" not in st.session_state:
    st.session_state.positions = {"Fahad": 1, "Jawad": 1, "Arslan": 1, "Raza": 1}
    st.session_state.current_index = 0
    st.session_state.round_num = 1
    st.session_state.winner = None
    st.session_state.last_roll = None

players = ["Fahad", "Jawad", "Arslan", "Raza"]
emojis = ["🔴", "🔵", "🟢", "🟡"]
hex_colors = ["#ff3366", "#3388ff", "#33ff99", "#ffee33"]

st.markdown("""
<style>
    .big-title {font-size: 62px; background: linear-gradient(90deg,#ff00cc,#00ffcc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center;}
    .square {width:72px; height:72px; background:#222; border:4px solid #ffd700; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; font-size:14px; box-shadow:0 0 15px #ffd700;}
    .token {width:32px; height:32px; border-radius:50%; font-size:22px; box-shadow:0 0 12px currentColor; border:3px solid #111;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="big-title">POWERDICE LUDO</h1>', unsafe_allow_html=True)
st.markdown("**Fahad • Jawad • Arslan • Raza** — Ludo King style visuals with your exact rules", unsafe_allow_html=True)

if st.session_state.winner:
    st.balloons()
    st.success(f"🏆 {st.session_state.winner} WINS THE GAME! 🏆")
    if st.button("🔄 PLAY AGAIN", type="primary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
else:
    current = players[st.session_state.current_index]
    
    # Player panels (Ludo style)
    cols = st.columns(4)
    for i, p in enumerate(players):
        with cols[i]:
            pos = st.session_state.positions[p]
            st.subheader(f"{emojis[i]} {p}")
            st.progress(pos / 16)
            st.metric("Position", pos, label_visibility="collapsed")
    
    # The Track – exact Ludo King look
    st.subheader("🎮 THE TRACK (1 → 16)")
    track_cols = st.columns(16)
    for i in range(16):
        pos_num = i + 1
        with track_cols[i]:
            tokens = ""
            for j, p in enumerate(players):
                if st.session_state.positions[p] == pos_num:
                    tokens += f'<span class="token" style="background:{hex_colors[j]};">{emojis[j]}</span>'
            st.markdown(f"""
            <div class="square">
                <div style="color:#ffd700; font-weight:bold;">{pos_num}</div>
                <div style="display:flex; gap:4px; flex-wrap:wrap; justify-content:center;">{tokens}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Power & Dice section
    st.markdown(f"### ROUND {st.session_state.round_num} — 🔥 POWER PLAYER: **{current} {emojis[players.index(current)]}**")
    
    if st.button(f"🎲 ROLL SPECIAL DICE FOR {current}", type="primary", use_container_width=True):
        roll = random.choice([1, 2, -1, -2])
        st.session_state.last_roll = roll
        
        # Animation effect
        with st.spinner("Rolling the power dice..."):
            time.sleep(0.8)
        
        # Apply moves exactly as you described
        for p in players:
            if st.session_state.positions[p] < 16:
                st.session_state.positions[p] += 1
        
        # Extra move for power player
        after_base = st.session_state.positions[current]
        if after_base + roll <= 16:
            st.session_state.positions[current] += roll
        
        # Clamp
        for p in players:
            if st.session_state.positions[p] < 1:
                st.session_state.positions[p] = 1
        
        # Check winner
        for p in players:
            if st.session_state.positions[p] == 16:
                st.session_state.winner = p
                break
        
        # Next power
        st.session_state.current_index = (st.session_state.current_index + 1) % 4
        st.session_state.round_num += 1
        st.rerun()
    
    if st.session_state.last_roll is not None:
        color = "🟢" if st.session_state.last_roll > 0 else "🔴"
        st.markdown(f"**Last roll:** {st.session_state.last_roll:+d} {color * abs(st.session_state.last_roll)}")

# Rules (collapsible like real games)
with st.expander("📜 How to Play (your exact rules)"):
    st.write("""
    - Everyone starts at position **1**  
    - Every round: **+1 base move** for ALL 4 players (exact landing on 16 required)  
    - Power player rolls the **special dice** (+1 / +2 green or -1 / -2 red)  
    - Extra move only applied if it doesn't overshoot 16  
    - First to land **exactly** on 16 wins  
    - Turn order: Fahad → Jawad → Arslan → Raza → repeat
    """)

st.caption("Built for Fahad in Karachi • Full Ludo King style layout • Ready for Streamlit Cloud")
