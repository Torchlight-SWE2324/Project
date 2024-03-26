import streamlit as st

class ViewUtente:
    """
        def __init__(self, controller):
            self.controller = controller

            st.title("ChatSQL")
            st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
            st.sidebar.title("Login sidebar")
            self.username = st.sidebar.text_input("Username")
            self.password = st.sidebar.text_input("Password", type="password")
            clickLogin = st.sidebar.button("Login")
            if clickLogin: #se viene schiacciato bottone chiamo funzione OperazioneLogin
                self.controller.login(self.username, self.password)
    """

    def __init__(self):
        self._controller = None
        """self.username = None
        self.password = None"""

        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        st.sidebar.title("Login sidebar")
        self.username_input = st.sidebar.text_input("Username")
        self.password_input = st.sidebar.text_input("Password", type="password")
        self.click_login_button = st.sidebar.button("Login")
        
        if self.click_login_button:
            self.login_handler()

    def initialize(self, controller):
        self._controller = controller
    
    def login_handler(self):
        print(f"Username: {self.username_input}, Password: {self.password_input}")
        self._controller.login(self.username_input, self.password_input)
    
    """def getUserPass(self):
        return self.username, self.password"""
    
    def loginSucc(self):
        st.success("Login avvenuto con successo")

    def loginErr(self):
        st.error("Login sbagliato")

    def loginMancante(self):
        st.warning("Inserisci prima Username e Password")

    def setController(self, controller):
        self.controller = controller

class ViewTecnico:
    pass


class ViewChat:
    pass