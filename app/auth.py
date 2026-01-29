import streamlit as st
from app.config import PACKAGE_FEATURES, PACKAGE_TYPE
import os

def logout(preserve_chat=True):
    chat_history = st.session_state.get("chat_history", []) if preserve_chat else []

    st.session_state.clear()

    if preserve_chat:
        st.session_state.chat_history = chat_history

    st.session_state.logged_in = False
    st.session_state.role = "user"
    st.rerun()

def login():
    features = PACKAGE_FEATURES[PACKAGE_TYPE]

    if not features["auth"]:
        st.session_state.role = "user"
        st.session_state.logged_in = True
        return

    st.title("Login")
    
    if "role" not in st.session_state:
        role = st.selectbox("Login as", ["user", "admin"])
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

            if role == "admin" and password != ADMIN_PASSWORD:
                st.error("Invalid admin password")
            else:
                st.session_state.role = role
                st.session_state.logged_in = True
                st.success(f"Logged in as {role}")
                st.rerun()
    
    else:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.success(f"Logged in as {st.session_state.role}")

        with col2:
            if st.button("🚪 Logout"):
                logout(preserve_chat=True)
                
    