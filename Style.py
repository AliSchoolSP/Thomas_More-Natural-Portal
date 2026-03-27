import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .title-container {
            border: 4px solid #ff9100;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            margin: 50px auto;
            max-width: 800px;
        }
        
        .stApp {
            background-color: #ffffff;
        }

        [data-testid="stSidebar"] {
            background-color: #f0f2f6 !important;
            border-right: 1px solid #d1d5db;
        }

        h1, h2, h3 {
            color: #003d7c !important;
            font-family: 'Source Sans Pro', sans-serif;
        }

        div.stButton > button {
            background-color: #ff9100 !important;
            color: white !important;
            border-radius: 5px;
            border: none;
            width: 100%;
        }

        button[kind="secondary"] {
            background-color: #ff4b4b !important;
        }
        </style>
    """, unsafe_allow_html=True)