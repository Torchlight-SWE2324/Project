import streamlit as st
from model import *

class View():
    def __init__(self):
        self._model = Model()
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")

    
    def technician_login(self):
        st.sidebar.title("Login sidebar")
        usernameSidebar = st.sidebar.text_input("Username")
        passwordSidebar = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if (self._model.checkLogin(usernameSidebar, passwordSidebar)):
                st.success("Login successful!")
            else:
                st.error("Login failed. Invalid username or password.")    
            #return [usernameSidebar, passwordSidebar]