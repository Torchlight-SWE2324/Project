import streamlit as st
from controller import *

class View:
    def __init__(self, controller):
        self._controller = controller
        self.username = None
        self.password = None

        self.titleS = st.sidebar.empty()
        self.usernameS = st.sidebar.empty()
        self.passwordS = st.sidebar.empty()
        self.loginS = st.sidebar.empty()

    def display_data(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        self.titleS.title("Login sidebar")
        """self.chat()"""
        self.username = self.usernameS.text_input("Username")
        self.password = self.passwordS.text_input("Password", type="password")
        self.login_button = self.loginS.button("Login")
        if self.login_button:
            self._controller.updateLoginData(self.username, self.password)

    def esitoPositivo(self):
        st.success("Login avvenuto")
        self.usernameS.empty()
        self.passwordS.empty()
        self.loginS.empty()

    def esitoNegativo(self):
        st.error("Login sbagliato")

    def esitoMancante(self):
        st.warning("Inserisci Username e Password")

class ViewTecnico:
    def __init__(self, controller):
        self._controllerTecnico = controller
        self.fileUpload = None
        self.titleS = st.sidebar.empty()
        self.container_delete = st.sidebar.empty()
        self.button_delete = st.sidebar.empty()
        self.container_upload = st.sidebar.empty()
        self.button_upload = st.sidebar.empty()
        self.logoutS = st.sidebar.empty()

    def display_data(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        self.titleS.title("Sidebar Tecnico")
        self.uploadFile()
        self.deleteFile()
        self.logoutS.button("Logout")


    def uploadFile(self):
        uploaded_file = self.container_upload.file_uploader("Upload new data dictionary file", accept_multiple_files=False, type="json")
        self.button_upload.button("Upload file", type="primary", on_click=lambda:self.operazioneUpload(uploaded_file), disabled=uploaded_file == None)
 
    def operazioneUpload(self, file):
        print("FILE VIEW PASSATO")
        self.fileUpload = file
        self._controllerTecnico.updateFileData()

    def getFileUploaded(self):
        return self.fileUpload
    
    def esitoPositivo(self):
        st.success("Caricamento dizionario avvenuto con successo")

    def esitoNegativo(self):
        st.error("Dizionario non caricato :( ")

    def deleteFile(self):
        files = self._controllerTecnico.getFiles()
        file = self.container_delete.selectbox('Your data dictionary files', files, key="dizionari")
        clickSelectFile = self.button_delete.button("Delete selected file", type="primary", disabled=file == None)
        if clickSelectFile:  
            self._controllerTecnico.operazioneDelete(file)

    def esitoPositivoEliminazione(self):
        st.success("File eliminato")

    def esitoNegativoEliminazione(self):
        st.error("Eliminazione non avvenuta")



class ViewChat:
    def __init__(self, controller):
        self._controllerTecnico = controller
        self.chatContainer = st.container()
    
    def chat(self):
        self.chatUtente()

    def chatUtente(self):
        # Se non ho file nel db, non posso fare nulla e non posso visualizzare la chat
        if len(self._controllerTecnico.getFiles()) == 0:
            self.chatContainer.warning("No data dictionary files found. Please upload a file to continue.")
        else:
            self.chatContainer.chat_input("Type your query here", key="chat", max_chars=1000)
