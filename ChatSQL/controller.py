"""
This module defines the controllers of the application.
"""

import os.path
import time
import re

from widgets import st

class AuthenticationController:
    """
    Manages authentication operations.

    @param model: the model object
    @param view: the view object(=LoginWidget)
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operation_login(self):
        """
        Performs login operation.

        @param username: the username
        @param password: the password
        @return: None
        """
        username = self._view.get_username()
        password = self._view.get_password()
        if username == "" or password == "":
            self._view.missing_credential_outcome()
        else:
            esito = self._model.check_login(username, password)
            if esito:
                self._view.positive_login_outcome()
                time.sleep(.5)
                st.session_state.chat = []
                st.session_state.logged_in = True
                st.rerun()
            else:
                self._view.negative_login_outcome()

    def operation_get_logged_tate(self):
        """
        Gets the logged-in state.

        @return: the logged-in state
        """
        return self._model.get_logged_status()

    def set_view(self, view):
        """
        Sets the view object.

        @param view: the view object
        @return: None
        """
        self._view = view

class SelectionController:
    """
    Manages selection operations.

    @param model: the model object
    @param view: the view object(=SelectWidget)
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operation_get_all_dictionaries(self):
        """
        Gets all dictionaries.

        @return: all dictionaries as a list of Strings
        """
        return self._model.get_files_in_db()

    def operation_set_current_dictionary(self, dictionary):
        """
        Sets the current dictionary.

        @param dictionary: the dictionary to set
        @return: None
        """
        self._model.set_current_dictionary(dictionary)

    def set_view(self, view):
        """
        Sets the view object.

        @param view: the view object
        @return: None
        """
        self._view = view

class UploadController:
    """
    Manages file upload operations.

    @param model: the model object
    @param view: the view object(=UploadWidget)
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def __dictionary_check(self, uploaded_file) -> str:
        """
        Checks if the uploaded file is None, it's format and if it respects the schema defined by us.

        @param uploaded_file: the uploaded file
        @return: the result of the check
        """
        uploaded_file_name = uploaded_file.name
        if uploaded_file is None:
            return "File was not loaded, repeat attempt."

        if os.path.splitext(uploaded_file_name)[1] != ".json":
            return "File must have format JSON"

        if self._model.get_loaded_dictionaries_number() > 3:
            return "App cannot contain more than 4 dictionaries."

        for dictionary in self._model.get_all_dictionaries_names():
            if uploaded_file_name == dictionary:
                return f"File with name '{uploaded_file_name}' already present."
        return "successful_check"

    def operation_update_file_data(self):
        """
        Does the upload process, will update the view with the result

        @return: None
        """
        uploaded_file = self._view.get_file_uploaded()
        dictionary_check_result = self.__dictionary_check(uploaded_file)
        if dictionary_check_result == "successful_check":
            dictionary_content = uploaded_file.read()
            uploaded_file_content = dictionary_content.decode('utf-8')
            uploaded_file_name = uploaded_file.name
            dictionary_upload_result = self._model.upload_dictionary(uploaded_file_name, uploaded_file_content)
            if dictionary_upload_result == "upload_success":
                self._view.positive_upload_outcome(uploaded_file_name)
            else:
                self._view.negative_upload_outcome(dictionary_upload_result)
        else:
            self._view.negative_upload_outcome(dictionary_check_result)

    def set_view(self, view):
        """
        Sets the view object.

        @param view: the view object
        @return: None
        """
        self._view = view

class DeleteController:
    """
    Manages deletion operations.

    @param model: the model object
    @param view: the view object(=DeleteWidget)
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operation_delete(self, delete_file_name):
        """
        Deletes a file.

        @param delete_file_name: the file to delete
        @return: None
        """
        self._model.delete_file(delete_file_name)
        esito = self._model.get_elimination_outcome()
        if esito:
            self._view.positive_delete_outcome(delete_file_name)
            time.sleep(.5)
            st.rerun()
        else:
            self._view.negative_delete_outcome(delete_file_name)

    def set_view(self, view):
        """
        Sets the view object.

        @param view: the view object
        @return: None
        """
        self._view = view

class LogoutController:
    """
    Manages logout operations.

    @param model: the model object
    @param view: the view object(=LogoutWidget)
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operation_logout(self):
        """
        Performs logout operation.

        @return: None
        """
        self._model.set_logged_status(False)
        st.session_state.logged_in = self._model.get_logged_status()
        st.session_state.chat = []
        self._view.positive_logout_outcome()
        time.sleep(.5)
        st.rerun()

    def set_view(self, view):
        """
        Sets the view object.

        @param view: the view object
        @return: None
        """
        self._view = view

class ChatController:
    """
    Manages chat operations.

    @param chat_model: the chat model object
    @param select_model: the selection model object
    @param auth_model: the authentication model object
    @param view: the view object(=ChatWidget)
    """
    def __init__(self, chat_model, select_model, auth_model, view):
        self._chat_model = chat_model
        self._select_model = select_model
        self._auth_model = auth_model
        self._view = view

    def operation_generate_response(self):
        """
        Generates a response and shows it on the view.

        @return: None
        """
        user_input = self._view.get_user_input()
        sanitized_user_input = self.sanitize_input(user_input)
        current_dictionary = self._select_model.get_current_dictionary()
        if self._auth_model.get_logged_status():
            self._chat_model.generate_debug(user_input, sanitized_user_input, current_dictionary)
        else :
            self._chat_model.generate_prompt(user_input, sanitized_user_input, current_dictionary)
        gen_response = self._chat_model.get_response()
        self._view.show_response(gen_response)

    def operation_get_all_dictionaries(self):
        """
        Gets all dictionaries.

        @return: all dictionaries
        """
        return self._select_model.get_files_in_db()

    def sanitize_input(self, user_input):
        """
        Sanitizes user input.

        @param user_input: the user input
        @return: the sanitized input
        """
        return re.sub(r"['']", " ", user_input)

    def set_view(self, view):
        """
        Sets the view object.

        @param view: the view object
        @return: None
        """
        self._view = view
