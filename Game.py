import streamlit as st

def toon_spel():
    # We gebruiken de styling uit de hero-container voor een mooie titel
    st.markdown('<div class="hero-container"><h1>🎮 Nature Quest: Level Up!</h1></div>', unsafe_allow_html=True)
    
    # 1. Haal de huidige score op uit de centrale data (via session_state)
    xp = st.session_state.get('game_score', 0)
    
    # 2. Berekeningen voor Level en Progressie
    # Stel: elke 100 XP is een nieuw level
    level = (xp // 100) + 1
    xp_in_huidig_level = xp % 100
    progressie = xp_in_huidig_level / 100
    xp_nodig_voor_volgend = 100 - xp_in_huidig_level

    st.subheader(f"Welkom terug, Ranger!")
    
    # Gebruik st.metric voor een professionele look
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Huidig Level", f"Lvl {level}")
    with col2:
        st.metric("Totale XP", f"{xp} pts")
    with col3:
        st.metric("Volgend Level", f"{xp_nodig_voor_volgend} XP te gaan")

    # Voortgangsbalk
    st.write(f"Voortgang naar Level {level + 1}:")
    st.progress(progressie)
    
    st.divider()

    # 3. BADGES SYSTEEM (Visueel met st.info/success/warning)
    st.subheader("🏆 Jouw Badges")
    b1, b2, b3 = st.columns(3)

    with b1:
        # Altijd verdiend bij de start
        st.success("🌱 **Groentje**\n\nJe hebt je eerste stappen in de natuur gezet!")
        
    with b2:
        if xp >= 100:
            st.warning("🔍 **Natuur Detective**\n\nJe hebt succesvol objecten herkend met AI.")
        else:
            st.info(f"🔒 **Vergrendeld**\n\nVerzamel {100-xp} XP meer voor deze badge.")

    with b3:
        if xp >= 500:
            st.error("🦅 **Beschermheer**\n\nJe bent een expert in het beveiligen van de Kemp!")
        else:
            st.info(f"🔒 **Vergrendeld**\n\nVerzamel {500-xp} XP meer voor deze badge.")

    st.divider()

    # 4. LEADERBOARD (Simulatie van andere gebruikers)
    st.subheader("🥇 Top Rangers van de Week")
    
    # We maken een lijstje met fictieve spelers en voegen de huidige gebruiker toe
    leaderboard_data = [
        {"Naam": "Ranger Tom", "XP": 1250, "Level": 13},
        {"Naam": "Expert Sarah", "XP": 840, "Level": 9},
        {"Naam": "Jij", "XP": xp, "Level": level}
    ]
    
    # Sorteer op XP (hoogste eerst)
    sorted_leaderboard = sorted(leaderboard_data, key=lambda x: x['XP'], reverse=True)
    st.table(sorted_leaderboard)

    # Dagelijkse bonus knop
    if st.button("🎁 Claim Dagelijkse Bonus (+10 XP)"):
        st.session_state['game_score'] = st.session_state.get('game_score', 0) + 10
        st.balloons()
        st.rerun()