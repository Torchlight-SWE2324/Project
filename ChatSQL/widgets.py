import streamlit as st

from controller import *

class LoginWidget:
    def __init__(self, controller_aut):
        self._controller_aut = controller_aut

    def create(self):
         st.sidebar.header('Login in the technician section', divider='grey')
         self.username = st.sidebar.text_input("Username")
         self.password = st.sidebar.text_input("Password", type="password")
         self.login_button = st.sidebar.button("Login")
         
         if self.login_button:
             self._controller_aut.operationLogin(self.username, self.password)

    def positiveLoginOutcome(self):
        st.success('Login successfull!', icon="✅")

    def negativeLoginOutcome(self):
        st.error('Wrong credentials. Please try again.', icon="🚨")

    def missingCredentialOutcome(self):
        st.warning('Please write both username and password')

    def getController(self):
        return self._controller_aut
    
    def setController(self, controller):
        self._controller_aut = controller


class LogoutWidget:
    def __init__(self, controller_log):
        self._controller_logout = controller_log

    def create(self):
        st.sidebar.header('Leave the technician section', divider='grey')
        bottone_logout = st.sidebar.button("Logout")
        
        if bottone_logout:
            self._controller_logout.operationLogout()

    def positiveLogoutOutcome(self):
        st.success('Logged out', icon="✅")

    def getController(self):
        return self._controller_logout
    
    def setController(self, controller):
        self._controller_logout = controller


class SelectWidget:
    def __init__(self, controller_sel):
        self.__controller_sel = controller_sel
        self.__file = None

    def create(self):
        files = self.__controller_sel.operationGetAllDictionaries()
        file = st.sidebar.selectbox('Your data dictionary files', files, key="dizionari")
        self.__controller_sel.operationSetCurrentDictionary(file)
        self.__file = file

    def getFile(self):
        return self.__file

    '''
    def getController(self):
        return self.__controller_sel
    
    def setController(self, controller):
        self.__controller_sel = controller
    '''


class UploadWidget:
    def __init__(self, controller_up):
        self.__controller_up = controller_up
        self.__file_uploaded = None
        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 0

    def create(self):
        upload_this_file = st.sidebar.file_uploader("Upload new data dictionary file", accept_multiple_files=False, key = st.session_state["file_uploader_key"])
        st.sidebar.button("Upload file", type="primary", on_click=lambda:self.__operazioneUpload(upload_this_file), disabled=upload_this_file == None)

    def __operazioneUpload(self, upload_this_file):
        self.__file_uploaded = upload_this_file
        self.__controller_up.operationUpdateFileData()

    def getFileUploaded(self):
        return self.__file_uploaded

    def positiveUploadOutcome(self, uploaded_file_name):
        st.success(f'Dictionary "{uploaded_file_name}" uploaded.', icon="✅")
        st.session_state["file_uploader_key"] += 1

    def negativeUploadOutcome(self, dictionary_upload_error):
        st.error(dictionary_upload_error, icon="🚨")
        st.session_state["file_uploader_key"] += 1


class DeleteWidget:
    def __init__(self, selection_widget, controller_del):
        self._selection_widget = selection_widget
        self._controller_del = controller_del

    def create(self):
        self._selection_widget.create()
        delete_file_name = self._selection_widget.getFile()
        click_select_file = st.sidebar.button("Delete selected file", type="primary", disabled=delete_file_name == None)
        
        if click_select_file:  
            self._controller_del.operationDelete(delete_file_name)
    
    def positiveDeleteOutcome(self, deleted_file_name):
        st.success(f'Dictionary "{deleted_file_name}" deleted successfully.', icon="✅")

    def negativeDeleteOutcome(self, file_name):
        st.error(f'Deletion of dictionary "{file_name}" failed.', icon="🚨")

    def getSelWidget(self):
        return self._selection_widget
    
    def setSelWidget(self, sel_widget):
        self._selection_widget = sel_widget

    def getController(self):
        return self._controller_del
    
    def setController(self, controller):
        self._controller_del = controller


class ChatWidget:
    def __init__(self, controller_cha):
        self._controller_chat = controller_cha
        self._user_input = None
        self._current_dictionary = None

    def create(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        
        for message in st.session_state.chat:
            with st.chat_message(message["role"]):
                st.code(message["content"], language="markdown")

        if (self._controller_chat.operationGetAllDictionaries() == []):
            st.chat_input("A data dictionary has not been uploaded. Please log in as a technician to upload one.", disabled=True)  
        else:
            self._user_input = st.chat_input("Type your query here", max_chars=500)
            
            if self._user_input:
                st.write(f"User has sent the following prompt: {self._user_input}")
                
                self._controller_chat.operationGenerateResponse(self._user_input)

    def showResponse(self, gen_response):
        st.session_state.chat.append({"role": "user", "content": gen_response})
        st.code(f"Response: {gen_response}", language="markdown")


    def getController(self):
        return self._controller_chat
    
    def setController(self, controller):
        self._controller_chat = controller
