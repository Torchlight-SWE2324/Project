import os.path
import time
import re

from model import *
from widgets import *

class AuthenticationController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operationLogin(self, username, password):
        if username == "" or password == "":
            self._view.missingCredentialOutcome()
        else:
            esito = self._model.checkLogin(username, password)
            if esito:
                self._view.positiveLoginOutcome()
                time.sleep(.5)
                st.session_state.chat = []
                st.session_state.logged_in = True
                st.rerun()
            else:
                self._view.negativeLoginOutcome()

    def operationGetLoggedState(self):
        return self._model.getLoggedStatus()
    
    def getView(self):
        return self._view

    def setView(self, view):
        self._view = view
    
    def getModel(self):
        return self._model
    
    def setModel(self, model):
        self._model = model
        

class SelectionController:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

    def operationGetAllDictionaries(self):
        return self.__model.getFilesInDB()

    def operationSetCurrentDictionary(self, dictionary):
        self.__model.setCurrentDictionary(dictionary)

    def setView(self, view):
        self.__view = view
    '''
    def operationGetCurrentDictionary(self):
        return (self.__model.getCurrentDictionary())

    def getView(self):
        return self.__view
    
    def getModel(self):
        return self.__model
    
    def setModel(self, model):
        self.__model = model
    '''


class UploadController:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

    def __dictionaryCheck(self, uploaded_file) -> str:
        uploaded_file_name = uploaded_file.name
        
        if uploaded_file is None:
            return f'File was not loaded, repeat attempt.'
        
        if os.path.splitext(uploaded_file_name)[1] != ".json":
            return "File must have format JSON"

        if self.__model.getLoadedDictionariesNumber() > 3:
            return "App cannot contain more than 4 dictionaries."

        for dictionary in self.__model.getAllDictionariesNames():
            if uploaded_file_name == dictionary:
                return f'File with name "{uploaded_file_name}" already present.'

        return "successful_check"

    def operationUpdateFileData(self):
        uploaded_file = self.__view.getFileUploaded()
        dictionary_check_result = self.__dictionaryCheck(uploaded_file)

        if dictionary_check_result == "successful_check":
            dictionary_content = uploaded_file.read()
            uploaded_file_content = dictionary_content.decode('utf-8')
            uploaded_file_name = uploaded_file.name
            dictionary_upload_result = self.__model.uploadDictionary(uploaded_file_name, uploaded_file_content)
            
            if dictionary_upload_result == "upload_success":
                self.__view.positiveUploadOutcome(uploaded_file_name)
            else:
                self.__view.negativeUploadOutcome(dictionary_upload_result)
        else:
            self.__view.negativeUploadOutcome(dictionary_check_result)

    def setView(self, view):
        self.__view = view

    '''
    def getView(self):
        return self._view
    
    def getModel(self):
        return self.__model
    
    def setModel(self, model):
        self.__model = model
    '''


class DeleteController:
    def __init__(self, model, view):
        self._model = model
        self._view = view  

    def operationDelete(self, delete_file_name):
        self._model.deleteFile(delete_file_name)
        esito = self._model.getEliminationOutcome()
        if esito:
            self._view.positiveDeleteOutcome(delete_file_name)
            time.sleep(.5)
            st.rerun()
        else:
            self._view.negativeDeleteOutcome(delete_file_name)
    
    def getView(self):
        return self._view

    def setView(self, view):
        self._view = view
    
    def getModel(self):
        return self._model
    
    def setModel(self, model):
        self._model = model


class LogoutController:
    def __init__(self, model, view):
        self._model = model
        self._view = view  
    
    def operationLogout(self):
        self._model.setLoggedStatus(False)
        st.session_state.logged_in = self._model.getLoggedStatus()
        st.session_state.chat = []
        self._view.positiveLogoutOutcome()
        time.sleep(.5)
        st.rerun()

    def getView(self):
        return self._view

    def setView(self, view):
        self._view = view
    
    def getModel(self):
        return self._model
    
    def setModel(self, model):
        self._model = model


class ChatController:
    def __init__(self, chat_model, select_model, auth_model, view):  # chatModel, selModel, authModel
        self._chat_model = chat_model
        self._select_model = select_model
        self._auth_model = auth_model
        self._view = view

    def operationGenerateResponse(self, user_input):
        current_dictionary = self._select_model.getCurrentDictionary()
        sanitized_user_input = self.sanitizeInput(user_input)
        if self._auth_model.getLoggedStatus():
            self._chat_model.generateDebug(user_input, sanitized_user_input, current_dictionary)
        else :
            self._chat_model.generatePrompt(user_input, sanitized_user_input, current_dictionary)
        gen_response = self._chat_model.getResponse()    
        self._view.showResponse(gen_response)

    def operationGetAllDictionaries(self):
        return self._select_model.getFilesInDB()

    def sanitizeInput(self, user_input):
        return re.sub(r"['']", " ", user_input)
    
    def getView(self):
        return self._view

    def setView(self, view):
        self._view = view
    
    def getModel(self):
        return self._model
    
    def setModel(self, model):
        self._model = model