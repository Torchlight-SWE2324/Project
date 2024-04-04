import streamlit as st
from controller import *

class LoginWidget:
    def __init__(self, controllerAut):
        self._controllerAut = controllerAut

    def create(self):
        st.sidebar.header('Login in sezione tecnico', divider='grey')
        self.username = st.sidebar.text_input("Username")
        self.password = st.sidebar.text_input("Password", type="password")
        self.login_button = st.sidebar.button("Login")
        if self.login_button:
            self._controllerAut.updateLoginData(self.username, self.password)
    
    def esitoPositivo(self):
        st.success('LogIn avvenuto con successo!', icon="✅")

    def esitoNegativo(self):
        st.error('Credenziali sbagliate. Si prega di riprovare!', icon="🚨")

    def esitoMancante(self):
        st.warning('Inserisci prima username e password!', icon="🔥")


class LogoutWidget:
    def __init__(self, controllerLog):
        self._controllerLogout = controllerLog

    def create(self):
        st.sidebar.header('Lougout da sezione tecnico', divider='grey')
        bottone_logout = st.sidebar.button("Logout")
        if bottone_logout:
            self._controllerLogout.logout()
    
    def logoutEsito(self):
        st.success('LogOut avvenuto con successo!', icon="✅")


class SelectWidget:
    def __init__(self, controllerSel):
        self._controllerSel = controllerSel
        self._file = None

    def create(self):
        files = self._controllerSel.getFiles()
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
        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 0

    def create(self):
        uploaded_file = st.sidebar.file_uploader("Upload new data dictionary file", accept_multiple_files=False, key = st.session_state["file_uploader_key"])
        st.sidebar.button("Upload file", type="primary", on_click=lambda:self.operazioneUpload(uploaded_file), disabled=uploaded_file == None)

    def operazioneUpload(self, uploaded_file):
        self.fileUpload = uploaded_file
        self._controllerUp.updateFileData()

    def getFileUploaded(self):
        return self.fileUpload

    def esitoPositivo(self, uploaded_file_name):
        st.success(f'Dizionario "{uploaded_file_name}" caricato con successo!', icon="✅")
        st.session_state["file_uploader_key"] += 1

    def esitoNegativo(self, dictionary_upload_error):
        st.error(dictionary_upload_error, icon="🚨")


class DeleteWidget:
    def __init__(self, selectionWidget, controllerDel):
        self._selectionWidget = selectionWidget
        self._controllerDel = controllerDel

    def create(self):
        self._selectionWidget.create() #creo widget di selezione dentro al widget di delete
        file = self._selectionWidget.getFile()
        
        clickSelectFile = st.sidebar.button("Delete selected file", type="primary", disabled=file == None)
        if clickSelectFile:  
            self._controllerDel.operazioneDelete(file)
    
    def getSelWidget(self):
        return self._selectionWidget
    
    def esitoPositivoEliminazione(self, file_name):
        st.success(f'Dizionario "{file_name}" eliminato con successo!', icon="🗑️")

    def esitoNegativoEliminazione(self, file_name):
        st.error(f'Eliminazione di "{file_name}" non avvenuta!', icon="🚨")

class ChatWidget:
    def __init__(self, controllerCha, controllerSel, controllerAut):
        self._controllerChat = controllerCha
        self._controllerSel = controllerSel
        self._controllerAut = controllerAut
        self.user_input = None
        self.dizionarioAttuale = None

    def create(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        for message in st.session_state.chat:
            with st.chat_message(message["role"]):
                st.write(f'<div style="white-space: pre-line;">{message["content"]}</div>', unsafe_allow_html=True)

        if (self._controllerSel.getFiles() == []):
            st.chat_input(disabled=True)
        else:
            self.user_input = st.chat_input("Type your query here", max_chars=500)
            if self.user_input:
                st.write(f"User has sent the following prompt: {self.user_input}")
                if (self._controllerAut.getLoggedState() == False):
                    print("USER")
                    self.selectChatUtente()
                else:
                    print("TECNICO")
                    self.selectChatTecnico()

    def selectChatUtente(self):
        self.dizionarioAttuale = self._controllerSel.getDizionario()
        self._controllerChat.operazionePrompt(self.user_input, self.dizionarioAttuale)

    def selectChatTecnico(self):
        self.dizionarioAttuale = self._controllerSel.getDizionario()
        self._controllerChat.operazioneDebug(self.user_input, self.dizionarioAttuale)

    def showResponse(self, messaggio):
        st.session_state.chat.append({"role": "user", "content": messaggio})
        st.code(f"Response: {messaggio}", language="markdown")
