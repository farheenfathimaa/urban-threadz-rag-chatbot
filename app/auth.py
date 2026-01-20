import streamlit as st
from app.config import PACKAGE_FEATURES, PACKAGE_TYPE
import os

def login():
    features = PACKAGE_FEATURES[PACKAGE_TYPE]

    if not features["auth"]:
        st.session_state.role = "user"
        return

    if "role" not in st.session_state:
        st.title("Login")

        role = st.selectbox("Login as", ["user", "admin"])
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

            if role == "admin" and password != ADMIN_PASSWORD:
                st.error("Invalid admin password")
            else:
                st.session_state.role = role
                st.success(f"Logged in as {role}")
