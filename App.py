import streamlit as st
import pandas as pd
import Data, Style, Ai_model
import os

# Pagina instellingen
st.set_page_config(page_title="Thomas More Nature Portal", layout="wide")
Style.apply_custom_style()
Data.init_data()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- STARTPAGINA ---
if not st.session_state['logged_in']:
    st.markdown('<div class="title-container"><h1>🌿 Thomas More Nature Portal</h1></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        # DEEL 1: OFFICIEEL INLOGGEN
        st.subheader("🔐 Officieel Inloggen")
        u_name = st.text_input("Naam", placeholder="Typ je naam...")
        u_role = st.selectbox("Rol", ["Ranger", "Expert"]) 
        u_pass = st.text_input("Wachtwoord", type="password")
        
        if st.button("Aanmelden"):
            if u_pass == "SPADMIN":
                st.session_state.update({'logged_in': True, 'user_name': u_name, 'user_role': "Admin"})
                st.rerun()
            elif u_pass == "TM2026":
                st.session_state.update({'logged_in': True, 'user_name': u_name, 'user_role': u_role})
                st.rerun()
            else:
                st.error("Wachtwoord onjuist")
        
        st.divider() # Visuele scheiding tussen de twee delen

        # DEEL 2: GAST TOEGANG
        st.subheader("👁️ Gast Toegang")
        st.write("Wil je alleen even rondkijken?")
        if st.button("Doorgaan als Bezoeker"):
            st.session_state.update({'logged_in': True, 'user_name': "Gast", 'user_role': "Bezoeker"})
            st.rerun()

# --- INLOGGED STATUS ---
else:
    name = st.session_state['user_name']
    role = st.session_state['user_role']

    if name in st.session_state.get('muted_users', []) and role != "Admin":
        st.error("🚫 Je account is geblokkeerd."); st.stop()

    with st.sidebar:
        # Veilig logo laden
        logo = "Logo_Thomas_More.png"
        if os.path.exists(logo):
            try: st.image(logo, use_container_width=True)
            except: st.write("🏢 **Thomas More**")
        else:
            st.write("🏢 **Thomas More Geel**")

        avatars = {"Ranger": "🤠", "Expert": "🦌", "Admin": "🤖", "Bezoeker": "👤"}
        st.markdown(f"<h2 style='text-align:center;'>{avatars.get(role, '👤')}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>Gebruiker: <b>{name}</b></p>", unsafe_allow_html=True)
        st.divider()

        # Menu bepalen op basis van rol
        menu = ["Dashboard", "📍 Kaart"]
        if role != "Bezoeker":
            menu.insert(1, "📸 AI Scanner")
        
        if role == "Ranger": menu.append("🤠 Ranger Portaal")
        if role == "Expert": menu.append("🦌 Expert Portaal")
        if role == "Admin": menu.append("🤖 Admin Paneel")
        
        choice = st.radio("Navigatie", menu)
        
        st.divider()
        if st.button("🚪 Uitloggen"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- INHOUD ---
    if st.session_state.get('noodgeval'):
        st.error(f"🚨 **GEVAAR GEMELD:** {st.session_state['system_alert']}")

    if choice == "Dashboard":
        st.title("🏆 Leaderboard")
        if st.session_state['scores']:
            df = pd.DataFrame(list(st.session_state['scores'].items()), columns=['Naam', 'Punten']).sort_values('Punten', ascending=False)
            st.table(df)
        st.metric("Campus Status", st.session_state['campus_status'])

    elif choice == "📸 AI Scanner":
        Ai_model.toon_ai_dashboard()

    elif choice == "📍 Kaart":
        st.header("📍 Waarnemingen")
        obs = Data.get_observations()
        if obs: st.map(pd.DataFrame(obs)[['lat', 'lon']])
        else: st.info("Nog geen data op de kaart.")

    elif choice == "🤠 Ranger Portaal":
        st.header("🤠 Ranger Portaal")
        r_nood = st.text_input("Noodgeval beschrijving:")
        if st.button("🚨 MELD GEVAAR", type="secondary"):
            if r_nood:
                st.session_state.update({'noodgeval': True, 'system_alert': r_nood, 'campus_status': "🔴 GEVAAR"})
                Data.add_points(name, 50); st.rerun()

    elif choice == "🦌 Expert Portaal":
        st.header("🦌 Expert Portaal")
        if st.button("📊 Data opvragen (+20 ptn)"):
            st.info("Flora-index is stabiel."); Data.add_points(name, 20)

    elif choice == "🤖 Admin Paneel":
        st.header("🤖 Admin Paneel")
        t1, t2 = st.tabs(["📩 Inbox", "⚖️ Beheer"])
        with t1:
            if st.button("✅ Reset naar Veilig"):
                st.session_state.update({'noodgeval': False, 'system_alert': "", 'campus_status': "🟢 Veilig"}); st.rerun()
            for m in reversed(Data.get_messages()):
                st.info(f"**{m['van']}**: {m['bericht']}")