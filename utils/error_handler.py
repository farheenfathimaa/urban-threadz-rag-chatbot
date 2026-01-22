import streamlit as st
import logging
import traceback

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def handle_error(e: Exception):
    error_msg = str(e)

    # Always safe inside Streamlit
    st.error(error_msg)

    # Optional: print full traceback in console
    traceback.print_exc()


