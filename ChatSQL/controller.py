import os.path
import time
import re

#from model import *
from widgets import *

class AuthenticationController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operation_login(self, username, password):
        if username == "" or password == "":
            self._view.missing_credential_outcome()
        else:
            esito = self._model.checkLogin(username, password)
            if esito:
                self._view.positive_login_outcome()
                time.sleep(.5)
                st.session_state.chat = []
                st.session_state.logged_in = True
                st.rerun()
            else:
                self._view.negative_login_outcome()

    def operation_get_logged_tate(self):
        return self._model.getLoggedStatus()

    def get_view(self):
        return self._view

    def set_view(self, view):
        self._view = view

    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model

class SelectionController:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

    def operation_get_all_dictionaries(self):
        return self.__model.getFilesInDB()

    def operation_set_current_dictionary(self, dictionary):
        self.__model.setCurrentDictionary(dictionary)

    def set_view(self, view):
        self.__view = view

class UploadController:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

    def __dictionary_check(self, uploaded_file) -> str:
        uploaded_file_name = uploaded_file.name
        if uploaded_file is None:
            return "File was not loaded, repeat attempt."

        if os.path.splitext(uploaded_file_name)[1] != ".json":
            return "File must have format JSON"

        if self.__model.getLoadedDictionariesNumber() > 3:
            return "App cannot contain more than 4 dictionaries."

        for dictionary in self.__model.getAllDictionariesNames():
            if uploaded_file_name == dictionary:
                return f"File with name '{uploaded_file_name}' already present."
        return "successful_check"

    def operation_update_file_data(self):
        uploaded_file = self.__view.get_file_uploaded()
        dictionary_check_result = self.__dictionary_check(uploaded_file)
        if dictionary_check_result == "successful_check":
            dictionary_content = uploaded_file.read()
            uploaded_file_content = dictionary_content.decode('utf-8')
            uploaded_file_name = uploaded_file.name
            dictionary_upload_result = self.__model.uploadDictionary(uploaded_file_name, uploaded_file_content)
            if dictionary_upload_result == "upload_success":
                self.__view.positive_upload_outcome(uploaded_file_name)
            else:
                self.__view.negative_upload_outcome(dictionary_upload_result)
        else:
            self.__view.negative_upload_outcome(dictionary_check_result)

    def set_view(self, view):
        self.__view = view

class DeleteController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operation_delete(self, delete_file_name):
        self._model.deleteFile(delete_file_name)
        esito = self._model.getEliminationOutcome()
        if esito:
            self._view.positive_delete_outcome(delete_file_name)
            time.sleep(.5)
            st.rerun()
        else:
            self._view.negative_delete_outcome(delete_file_name)

    def get_view(self):
        return self._view

    def set_view(self, view):
        self._view = view

    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model

class LogoutController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operation_logout(self):
        self._model.setLoggedStatus(False)
        st.session_state.logged_in = self._model.getLoggedStatus()
        st.session_state.chat = []
        self._view.positive_logout_outcome()
        time.sleep(.5)
        st.rerun()

    def get_view(self):
        return self._view

    def set_view(self, view):
        self._view = view

    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model

class ChatController:
    def __init__(self, chat_model, select_model, auth_model, view):
        self._chat_model = chat_model
        self._select_model = select_model
        self._auth_model = auth_model
        self._view = view

    def operation_generate_response(self, user_input):
        current_dictionary = self._select_model.getCurrentDictionary()
        sanitized_user_input = self.sanitize_input(user_input)
        if self._auth_model.getLoggedStatus():
            self._chat_model.generateDebug(user_input, sanitized_user_input, current_dictionary)
        else :
            self._chat_model.generatePrompt(user_input, sanitized_user_input, current_dictionary)
        gen_response = self._chat_model.getResponse()
        self._view.show_response(gen_response)

    def operation_get_all_dictionaries(self):
        return self._select_model.getFilesInDB()

    def sanitize_input(self, user_input):
        return re.sub(r"['']", " ", user_input)

    def get_view(self):
        return self._view

    def set_view(self, view):
        self._view = view

    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model
