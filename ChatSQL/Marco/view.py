import streamlit as st
from model import *

class View():
    def __init__(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")

    def ask_user(self):
        return st.text_input("Inserisci un nuovo stato")

    def update(self, state):
        st.write(f"Stato aggiornato a: {state}")
        
    def technician_login(self):
        st.sidebar.title("Login sidebar")
        usernameSidebar = st.sidebar.text_input("Username")
        passwordSidebar = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            return usernameSidebar, passwordSidebar