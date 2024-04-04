import streamlit as st

from controller import *

class ViewUtente:
    def __init__(self, controllerAut, controllerSel):
        self._controllerAut = controllerAut
        self._controllerSel = controllerSel
        self.username = None
        self.password = None

        self.titleS = st.sidebar.empty()
        self.dizionariS = st.sidebar.empty()
        self.usernameS = st.sidebar.empty()
        self.passwordS = st.sidebar.empty()
        self.loginS = st.sidebar.empty()

    def display_data(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        self.titleS.title("Login as a Technician")
        self.selectDictionary()
        self.login()

    def selectDictionary(self):
        files = self._controllerSel.getFiles()
        file = self.dizionariS.selectbox('Your data dictionary files', files, key="dizionari")
        self._controllerSel.setDizionario(file)

    def login(self):
        self.username = self.usernameS.text_input("Username")
        self.password = self.passwordS.text_input("Password", type="password")
        self.login_button = self.loginS.button("Login")
        if self.login_button:
            self._controllerAut.updateLoginData(self.username, self.password)

    def esitoPositivo(self):
        st.success("Login successfull.")

    def esitoNegativo(self):
        st.error("The login was not successful.")

    def esitoMancante(self):
        st.warning("Please write username and password.")


class ViewTecnico:
    def __init__(self, controllerSel, controllerUp, controllerDel, controllerLogout):
        self._controllerSel = controllerSel
        self._controllerUp = controllerUp
        self._controllerDel = controllerDel
        self._controllerLogout = controllerLogout

        self.fileUpload = None
        self.containerNotifiche = st.sidebar.empty()
        self.containerNotifiche1 = st.sidebar.empty()
        self.titleS = st.sidebar.empty()
        self.container_delete = st.sidebar.empty()
        self.button_delete = st.sidebar.empty()
        self.container_upload = st.sidebar.empty()
        self.button_upload = st.sidebar.empty()
        self.logoutS = st.sidebar.empty()

    def display_data(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        self.titleS.title("Technician section")
        self.uploadFile()
        self.deleteFile()
        self.logout()

    def uploadFile(self):
        uploaded_file = self.container_upload.file_uploader("Upload new data dictionary file", accept_multiple_files=False, type="json")
        self.button_upload.button("Upload file", type="primary", on_click=lambda:self.operazioneUpload(uploaded_file), disabled=uploaded_file == None)
 
    def operazioneUpload(self, file):
        self.fileUpload = file
        self._controllerUp.updateFileData()

    def logout(self):    
        bottone_logout = self.logoutS.button("Logout")
        if bottone_logout:
            self._controllerLogout.logout()

    def logoutEsito(self):
        self.containerNotifiche.success("Successfully logged out")

    def getFileUploaded(self):
        return self.fileUpload
    
    def esitoPositivo(self):
        self.containerNotifiche.success("Dictionary loaded successfully")

    def esitoNegativo(self):
        self.containerNotifiche.error("Dictionary not uploaded")

    def deleteFile(self):
        files = self._controllerSel.getFiles()
        file = self.container_delete.selectbox('Your data dictionary files', files, key="dizionari")
        self._controllerSel.setDizionario(file)

        clickSelectFile = self.button_delete.button("Delete selected file", type="primary", disabled=file == None)
        if clickSelectFile:  
            self._controllerDel.operazioneDelete(file)

    def esitoPositivoEliminazione(self):
        self.containerNotifiche.success("File deleted successfully")

    def esitoNegativoEliminazione(self):
        self.containerNotifiche.error("The file has not been deleted")


class ViewChat:
    def __init__(self, controllerCha, controllerAut, controllerSel):
        self._controllerChat = controllerCha
        self._controllerAut = controllerAut
        self._controllerSel = controllerSel
        self.user_input = None
        self.dizionarioAttuale = None

    def display_data(self):
        self.user_input = st.chat_input("Type your query here", key="chat", max_chars=500)
        if self.user_input:
            st.write(f"User has sent the following prompt: {self.user_input}")
            self.selectChat()

    def selectChat(self):
        self.dizionarioAttuale = self._controllerSel.getDizionario()
        if self._controllerAut.getLoggedState():
            print("Logged as technician")
            self._controllerChat.operazioneDebug(self.user_input, self.dizionarioAttuale)
        else:
            print("Logged as user")
            self._controllerChat.operazionePrompt(self.user_input, self.dizionarioAttuale)

    def showResponse(self, messaggio):
        print("VIEW MESSAGGIO", messaggio)
        st.code(f"Response: {messaggio}", language="markdown")
