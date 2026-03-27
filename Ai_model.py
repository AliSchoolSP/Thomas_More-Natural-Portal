import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import os
import Data 

def get_assistant_avatar(role):
    """Geeft de juiste avatar URL terug gebaseerd op de rol."""
    if role == "Ranger":
        # Blije Ranger
        return "https://api.dicebear.com/7.x/avataaars/svg?seed=George&top=hat&clothing=shirtCrewNeck&clothingColor=3c533d&mouth=smile"
    elif role == "Expert":
        # Blije Bioloog
        return "https://api.dicebear.com/7.x/avataaars/svg?seed=Annabel&accessories=prescription02&clothing=overall&clothingColor=f5f5f5&mouth=smile"
    elif role == "Admin":
        # Admin Robot
        return "https://api.dicebear.com/7.x/bottts/svg?seed=Admin&backgroundColor=FC6900"
    else:
        # Bezoeker (Zakelijk/Aankoper)
        return "https://api.dicebear.com/7.x/avataaars/svg?seed=Oliver&top=shortHair&clothing=collarPolo&clothingColor=25557c&mouth=serious"

def toon_ai_dashboard():
    rol = st.session_state.get('user_role', 'Bezoeker')
    avatar_url = get_assistant_avatar(rol)

    st.markdown('<div class="hero-container"><h1>📸 AI Nature Scanner</h1></div>', unsafe_allow_html=True)
    
    # Assistent weergave
    col_av, col_txt = st.columns([1, 4])
    with col_av:
        st.image(avatar_url, width=100)
    with col_txt:
        if rol == "Admin":
            st.info("Systeembeheerder modus: Scan gereed voor diepe analyse.")
        elif rol == "Ranger":
            st.success("Hé Ranger! Laat me die foto zien, dan check ik het gebied direct.")
        elif rol == "Expert":
            st.warning("Klaar voor veldonderzoek? Upload je monster voor classificatie.")
        else:
            st.info("Welkom! Maak een foto van de natuur en ik help je bij de identificatie.")

    model_path = "keras_model.h5"
    label_path = "labels.txt"

    # Input opties
    bron = st.radio("Kies bron:", ["📸 Camera", "📁 Upload"], horizontal=True)
    upload = st.camera_input("Scan") if bron == "📸 Camera" else st.file_uploader("Kies een afbeelding")

    if upload:
        image = Image.open(upload).convert("RGB")
        
        if st.button("🚀 Start Analyse", use_container_width=True):
            with st.spinner("AI analyseert..."):
                try:
                    import tensorflow as tf
                    # Forceer geheugen vrijgave
                    tf.keras.backend.clear_session()
                    
                    # Fix voor Teachable Machine lagen
                    class FixedDepthwise(tf.keras.layers.DepthwiseConv2D):
                        def __init__(self, *args, **kwargs):
                            kwargs.pop('groups', None)
                            super().__init__(*args, **kwargs)

                    # Laad het model
                    model = tf.keras.models.load_model(
                        model_path, 
                        compile=False, 
                        custom_objects={'DepthwiseConv2D': FixedDepthwise}
                    )

                    # Afbeelding voorbereiden (224x224)
                    size = (224, 224)
                    image_res = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
                    img_array = np.asarray(image_res).astype(np.float32)
                    normalized = (img_array / 127.5) - 1
                    
                    # Maak een schone batch van 1
                    final_input = np.expand_dims(normalized, axis=0)

                    # --- DE DEFINITIEVE FIX ---
                    # Gebruik .call() met training=False om de '2 tensors' error te voorkomen
                    prediction_tensor = model(final_input, training=False)
                    prediction = prediction_tensor.numpy() if hasattr(prediction_tensor, 'numpy') else prediction_tensor
                    
                    index = np.argmax(prediction[0])
                    
                    with open(label_path, "r") as f:
                        class_names = [l.strip() for l in f.readlines()]
                    
                    label_naam = class_names[index][2:]
                    confidence = prediction[0][index]

                    # Resultaat tonen
                    st.divider()
                    st.balloons()
                    st.subheader(f"✅ Analyse Compleet")
                    
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.metric("Gevonden", label_naam)
                    with res_col2:
                        st.metric("Zekerheid", f"{round(confidence * 100)}%")
                    
                    # Data opslaan
                    Data.save_ai_result(label_naam, confidence, upload)

                except Exception as e:
                    st.error(f"Fout tijdens analyse: {e}")
                    st.info("Probeer de pagina te vernieuwen of herstart de terminal.")
