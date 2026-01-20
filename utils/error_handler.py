import streamlit as st
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def handle_error(error: Exception, user_message: str = "Something went wrong."):
    logging.error(str(error))

    if st._is_running_with_streamlit:
        st.error(user_message)
