# view.py

import streamlit as st
import time

def display_chat_message(role, content):
    with st.chat_message(role):
        st.markdown(content)

def display_spinner(text):
    with st.spinner(text):
        time.sleep(1)  # Just for demonstration purposes

def display_code(content):
    st.code(content, language='markdown')

def display_chat_input(placeholder, disabled=False):
    return st.chat_input(placeholder, disabled=disabled)
