import streamlit as st

def render_chat_ui():
    st.title("📦 Business Document Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question about the business...")

    return user_input


def add_message(role, content):
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })
