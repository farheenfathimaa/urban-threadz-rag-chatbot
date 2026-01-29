import streamlit as st
import json
from pathlib import Path
import time
import base64

def load_business_config(business_id: str):
    path = Path(f"businesses/{business_id}/business.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_audio_base64(audio_path):
    """Convert audio file to base64 for HTML embedding"""
    try:
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        return base64.b64encode(audio_bytes).decode()
    except:
        return None

def show_splash_screen(business_config):
    """Show animated splash screen with logo morphing effect (NO SOUND)"""

    branding = business_config.get("branding", {})
    logo_url = branding.get("logo_url")

    if not logo_url:
        return  # Skip splash if no logo

    logo_file = Path(f"businesses/{business_config['business_id']}/{logo_url}")
    if not logo_file.exists():
        return

    # Convert logo to base64
    with open(logo_file, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

    splash_html = f"""
    <style>
        /* Hide all Streamlit elements during splash */
        [data-testid="stAppViewContainer"] > section {{
            opacity: 0;
        }}

        @keyframes popIn {{
            0% {{
                opacity: 0;
                transform: scale(0.2);
            }}
            70% {{
                transform: scale(1.15);
            }}
            100% {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        @keyframes expandToFullScreen {{
            0% {{
                width: 300px;
                height: 300px;
                border-radius: 50%;
            }}
            100% {{
                width: 200vw;
                height: 200vh;
                border-radius: 0;
            }}
        }}

        @keyframes shrinkToLogo {{
            0% {{
                width: 200vw;
                height: 200vh;
                border-radius: 0;
            }}
            100% {{
                width: 300px;
                height: 300px;
                border-radius: 50%;
            }}
        }}

        @keyframes fadeOut {{
            0% {{
                opacity: 1;
            }}
            100% {{
                opacity: 0;
            }}
        }}

        .splash-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 99999;
            overflow: hidden;
        }}

        .splash-logo-container {{
            width: 300px;
            height: 300px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f5f5dc;
            border-radius: 50%;
            position: relative;
            animation:
                popIn 1s ease-out,
                expandToFullScreen 1.2s ease-in-out 1.2s forwards,
                shrinkToLogo 1.2s ease-in-out 4.4s forwards;
        }}

        .splash-logo {{
            max-width: 70%;
            max-height: 70%;
            object-fit: contain;
            filter: drop-shadow(0 0 20px rgba(0,0,0,0.3));
            z-index: 2;
        }}

        .splash-fade-out {{
            animation: fadeOut 0.6s ease-in-out 5.8s forwards;
        }}
    </style>

    <div class="splash-overlay splash-fade-out" id="splashScreen">
        <div class="splash-logo-container">
            <img src="data:image/png;base64,{logo_base64}" class="splash-logo" alt="Logo">
        </div>
    </div>

    <script>
        (function() {{
            setTimeout(function() {{
                var splash = document.getElementById('splashScreen');
                var appContent = document.querySelector('[data-testid="stAppViewContainer"] > section');

                if (splash) {{
                    splash.remove();
                }}
                if (appContent) {{
                    appContent.style.opacity = '1';
                    appContent.style.transition = 'opacity 0.3s ease-in';
                }}
            }}, 6400);
        }})();
    </script>
    """

    placeholder = st.empty()
    with placeholder.container():
        st.markdown(splash_html, unsafe_allow_html=True)

    time.sleep(6.5)  # keep timing exactly as requested
    placeholder.empty()

    
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
