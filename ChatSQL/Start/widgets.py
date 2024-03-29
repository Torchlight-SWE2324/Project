import streamlit as st
from controller import *

class LoginWidget:
    def __init__(self, controllerAut):
        self._controllerAut = controllerAut
        #self.usernameS = st.sidebar.empty()
        #self.passwordS = st.sidebar.empty()
        #self.loginS = st.sidebar.empty()
        self.usernameS = st.sidebar
        self.passwordS = st.sidebar
        self.loginS = st.sidebar
                
    #def login(self):
        self.username = self.usernameS.text_input("Username")
        self.password = self.passwordS.text_input("Password", type="password")
        self.login_button = self.loginS.button("Login")
        if self.login_button:
            self._controllerAut.updateLoginData(self.username, self.password)
    
    def esitoPositivo(self):
        st.sidebar.success("Login avvenuto")

    def esitoNegativo(self):
        st.sidebar.error("Login sbagliato")

    def esitoMancante(self):
        st.sidebar.warning("Inserisci Username e Password")

class LogoutWidget:
    def __init__(self, controllerLog):
        self._controllerLogout = controllerLog
        self.logoutS = st.sidebar.empty()

    def logout(self):  
        bottone_logout = self.logoutS.button("Logout")
        if bottone_logout:
            self._controllerLogout.logout()
    
    def logoutEsito(self):
        st.sidebar.success("Logout avvenuto con successo")

class SelectWidget:
    def __init__(self, controllerSel):
        self._controllerSel = controllerSel
        #self.dizionariS =  st.sidebar.empty()
        self._file = None
        
    #def selectDictionary(self):
        files = self._controllerSel.getFiles()
        #file = self.dizionariS.selectbox('Your data dictionary files', files, key="dizionari")
        file = st.sidebar.selectbox('Your data dictionary files', files, key="dizionari")
        self._controllerSel.setDizionario(file)
        self._file = file
    
    def getController(self):
        return self._controllerSel
    
    def getFile(self):
        return self._file

class UploadWidget:
    def __init__(self, controllerUp):
        self._controllerUp = controllerUp
        uploaded_file = self.container_upload.file_uploader("Upload new data dictionary file", accept_multiple_files=False, type="json")
        self.button_upload.button("Upload file", type="primary", on_click=lambda:self.operazioneUpload(uploaded_file), disabled=uploaded_file == None)

    def esitoPositivo(self):
        st.sidebar.success("Caricamento dizionario avvenuto con successo")

    def esitoNegativo(self):
        st.sidebar.error("Dizionario non caricato :( ")

class DeleteWidget:
    def __init__(self, selectionWidget, controllerDel):
        self._selectionWidget = selectionWidget
        self._controllerDel = controllerDel
        self.container_delete = st.sidebar.empty()
        self.button_delete = st.sidebar.empty()

        self._selectionWidget.selectDictionary()
        file = self._selectionWidget.getFile()

        clickSelectFile = self.button_delete.button("Delete selected file", type="primary", disabled=file == None)
        if clickSelectFile:  
            self._controllerDel.operazioneDelete(file)
    
    def getSelWidget(self):
        return self._selectionWidget
    
    def esitoPositivoEliminazione(self):
       st.sidebar.success("File eliminato")

    def esitoNegativoEliminazione(self):
        st.sidebar.error("Eliminazione non avvenuta")

class ChatWidget:
    def __init__(self, controllerCha, controllerAut, controllerSel):
        self._controllerChat = controllerCha
        self._controllerAut = controllerAut
        self._controllerSel = controllerSel
        self.user_input = None
        self.dizionarioAttuale = None
        self.user_input = st.chat_input("Type your query here", key="chat", max_chars=500)
        if self.user_input:
            st.write(f"User has sent the following prompt: {self.user_input}")
            

    def selectChatUtente(self):
        self.dizionarioAttuale = self._controllerSel.getDizionario()
        self._controllerChat.operazioneDebug(self.user_input, self.dizionarioAttuale)

    def selectChatTecnico(self):
        self.dizionarioAttuale = self._controllerSel.getDizionario()
        self._controllerChat.operazionePrompt(self.user_input, self.dizionarioAttuale)

    def showResponse(self, messaggio):
        st.code(f"Response: {messaggio}", language="markdown")
