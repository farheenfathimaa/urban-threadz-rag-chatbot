import streamlit as st
import json
from pathlib import Path

def load_business_config(business_id: str):
    path = Path(f"businesses/{business_id}/business.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_chat_ui(business_config):
    branding = business_config.get("branding", {})

    primary = branding.get("primary_color", "#4CAF50")
    secondary = branding.get("secondary_color", "#1E1E1E")
    accent = branding.get("accent_color", "#C2A875")

    st.markdown(
        f"""
        <style>
        /* Main app background */
        [data-testid="stAppViewContainer"] {{
            background-color: {secondary};
        }}

        /* Chat messages */
        .stChatMessage[data-testid="chat-message-assistant"] {{
            background-color: #161B22;
            border-left: 4px solid {accent};
            border-radius: 10px;
            padding: 12px;
        }}

        .stChatMessage[data-testid="chat-message-user"] {{
            background-color: {primary};
            color: white;
            border-radius: 10px;
            padding: 12px;
        }}

        /* Headers */
        h1, h2, h3 {{
            color: {primary};
        }}

        /* Buttons */
        .stButton>button {{
            background-color: {primary};
            color: white;
            border-radius: 8px;
            border: none;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: #0E1117;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    logo_url = branding.get("logo_url")
    business_name = business_config.get("business_name", "Business")
    
    # 🧠 Header
    col1, col2 = st.columns([1, 6])
    with col1:
        if logo_url:
            logo_file = Path(f"businesses/{business_config['business_id']}/{logo_url}")
            if logo_file.exists():
                st.image(str(logo_file), width=60)
    with col2:
        st.markdown(
            f"<h1 style='margin-top: 10px;'>{business_name} Chatbot</h1>",
            unsafe_allow_html=True
        )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    return st.chat_input("Ask a question about the business...")

def add_message(role, content):
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })
