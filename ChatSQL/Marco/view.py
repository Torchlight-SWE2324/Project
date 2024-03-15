import streamlit as st
from observer import *
from subject import *
class View(Observer, Subject):
    def __init__(self, model):
        Subject.__init__(self)
        Observer.__init__(self)
        self._model = model
        self.username = None
        self.password = None
        self.isLogged = False
        self.ultimaOperazione = None
        self.button_command_map = {}

    def sezioneUtente(self):  
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        self.sideBarUtente()
        self.chatUtente()

    def sideBarUtente(self):
        st.sidebar.title("Login sidebar")
        self.username = st.sidebar.text_input("Username")
        self.password = st.sidebar.text_input("Password", type="password")
        clickLogin = st.sidebar.button("Login")
        if clickLogin: #se viene schiacciato bottone chiamo funzione OperazioneLogin
            self.operazioneLogin() 

    def chatUtente(self):
        pass
    
    def initialize_commands(self):  
        self.button_command_map["login"] = self.esitoLogin   

    def update(self):
        if self.ultimaOperazione in self.button_command_map:
            command = self.button_command_map[self.ultimaOperazione]
            command()

#operazione login
    def operazioneLogin(self):
        if self.username != None or self.password != None:
            self.ultimaOperazione= "login"
            self.notify_observers()

    def esitoLogin(self):
        if self._model.getIsLogedd():   # valore dentro al model                                    
            self.isLogged = True
            st.success("Login successful!")
        else:
            if self.isLogged == False: # valore dentro alla view
                st.error("Login non avvenuto con successo")
            else: 
                self.isLogged = False
                st.success("Logout successful!")

    def getUser(self):
        return [self.username, self.password]
    
    def getOperazione(self):
        return self.ultimaOperazione