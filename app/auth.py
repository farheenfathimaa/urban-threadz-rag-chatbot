import streamlit as st
from app.config import PACKAGE_FEATURES, PACKAGE_TYPE
import os

def logout(preserve_chat=True):
    # Save current role's chat history before clearing
    if preserve_chat and "role" in st.session_state:
        current_role = st.session_state.role
        chat_history = st.session_state.get("chat_history", [])
        
        # Store in role-specific key
        if current_role == "admin":
            st.session_state.admin_chat_history = chat_history
        else:
            st.session_state.user_chat_history = chat_history

    # Clear session state
    admin_chat = st.session_state.get("admin_chat_history", [])
    user_chat = st.session_state.get("user_chat_history", [])
    
    # ✅ Remove ONLY auth-related keys
    keys_to_remove = [
        "logged_in",
        "role",
        "chat_history",
        "is_admin",
        "admin_logged_in",
        "admin_user",
        "admin_email",
    ]

    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
    
    # Restore role-specific chat histories
    if preserve_chat:
        st.session_state.admin_chat_history = admin_chat
        st.session_state.user_chat_history = user_chat

    st.rerun()

def login():
    features = PACKAGE_FEATURES[PACKAGE_TYPE]

    if not features["auth"]:
        st.session_state.role = "user"
        st.session_state.logged_in = True
        return

    st.title("Login")
    
    if not st.session_state.get("logged_in", False):
        role = st.selectbox("Login as", ["user", "admin"])
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

            if role == "admin" and password != ADMIN_PASSWORD:
                st.error("Invalid admin password")
            else:
                st.session_state.role = role
                st.session_state.logged_in = True
                
                # Load role-specific chat history
                if role == "admin":
                    st.session_state.chat_history = st.session_state.get("admin_chat_history", [])
                else:
                    st.session_state.chat_history = st.session_state.get("user_chat_history", [])
                
                st.success(f"Logged in as {role}")
                st.rerun()
    
    else:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.success(f"Logged in as {st.session_state.role}")

        with col2:
            if st.button("🚪 Logout"):
                logout(preserve_chat=True)
                
    