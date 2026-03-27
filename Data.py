import streamlit as st
from datetime import datetime, timedelta
import hashlib

def init_data():
    if 'observations' not in st.session_state:
        st.session_state['observations'] = []
    if 'used_photo_hashes' not in st.session_state:
        st.session_state['used_photo_hashes'] = set()
    if 'last_scan_time' not in st.session_state:
        st.session_state['last_scan_time'] = {} 
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'user_log' not in st.session_state:
        st.session_state['user_log'] = []
    if 'muted_users' not in st.session_state:
        st.session_state['muted_users'] = set()
    if 'campus_status' not in st.session_state:
        st.session_state['campus_status'] = "🟢 Veilig"
    if 'noodgeval' not in st.session_state:
        st.session_state['noodgeval'] = False
    if 'system_alert' not in st.session_state:
        st.session_state['system_alert'] = ""
    if 'admin_broadcast' not in st.session_state:
        st.session_state['admin_broadcast'] = ""
    if 'scores' not in st.session_state:
        st.session_state['scores'] = {}

def add_points(naam, punten):
    if naam not in st.session_state['scores']:
        st.session_state['scores'][naam] = 0
    st.session_state['scores'][naam] += punten

def straf_gebruiker(naam, type_straf):
    if naam in st.session_state['scores']:
        if type_straf == "test":
            st.session_state['scores'][naam] -= 100
        elif type_straf == "pesten":
            st.session_state['scores'][naam] = 0
    st.session_state['muted_users'].add(naam)

def save_ai_result(vondst, confidence, image_file):
    # CHECK: Is image_file wel echt een geüpload bestand?
    if image_file is None or isinstance(image_file, str):
        st.error("Oeps! Er is geen geldige afbeelding gevonden om te verwerken.")
        return False

    naam = st.session_state.get('user_name', 'Gast')
    nu = datetime.now()
    
    # Nu pas proberen we de bytes op te halen
    try:
        file_bytes = image_file.getvalue()
    except AttributeError:
        st.error("Fout bij het lezen van het fotobestand.")
        return False

    photo_hash = hashlib.md5(file_bytes).hexdigest()
    # ... rest van je code ...

    # Anti-spam & Anti-copy checks
    if (naam in st.session_state['last_scan_time'] and (nu - st.session_state['last_scan_time'][naam]) < timedelta(seconds=30)):
        st.error("⏳ Wacht 30 seconden tussen scans.")
        return False
    if photo_hash in st.session_state['used_photo_hashes']:
        st.error("🚫 Deze foto is al gebruikt!")
        return False

    st.session_state['used_photo_hashes'].add(photo_hash)
    st.session_state['last_scan_time'][naam] = nu
    st.session_state['observations'].append({
        "tijd": nu.strftime("%H:%M"), "gebruiker": naam, "vondst": vondst,
        "lat": 51.1606, "lon": 4.9612
    })
    add_points(naam, 150)
    return True

def log_user(naam, rol):
    tijd = datetime.now().strftime("%H:%M")
    st.session_state['user_log'].append({"Tijd": tijd, "Naam": naam, "Rol": rol})
    if naam not in st.session_state['scores']: st.session_state['scores'][naam] = 0

def send_message(afzender, rol, tekst):
    if tekst.strip():
        st.session_state['messages'].append({
            "tijd": datetime.now().strftime("%H:%M"),
            "van": afzender, "rol": rol, "bericht": tekst
        })
        return True
    return False

def get_messages(): return st.session_state.get('messages', [])
def get_observations(): return st.session_state.get('observations', [])
