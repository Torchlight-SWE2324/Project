"""
This module defines various Streamlit widgets and their functionalities.

This module contains classes that define various widgets used in a Streamlit application for handling user interactions,
file uploads, deletions, and chat functionalities.
"""

import streamlit as st

class LoginWidget:
    """
    Widget for handling user login.

    This widget provides functionality for users to log in with their credentials and perform login-related actions.
    """

    def __init__(self, controller_aut):
        """
        Initialize the LoginWidget.

        @param controller_aut: The controller object for authentication operations.
        """
        self._controller_aut = controller_aut
        self.username = None
        self.password = None
        self.login_button = None

    def create(self):
        """
        Create the login widget.

        This method creates the login interface with input fields for username and password,
        along with a login button for submitting the credentials.
        """
        st.sidebar.header('Login in the technician section', divider='grey')
        self.username = st.sidebar.text_input("Username")
        self.password = st.sidebar.text_input("Password", type="password")
        self.login_button = st.sidebar.button("Login")
        if self.login_button:
            self._controller_aut.operation_login(self.username, self.password)

    def positive_login_outcome(self):
        """
        Show success message for login.

        This method displays a success message when the login operation is successful.
        """
        st.success('Login successful!', icon="✅")

    def negative_login_outcome(self):
        """
        Show error message for incorrect credentials.

        This method displays an error message when the user enters incorrect credentials during login.
        """
        st.error('Wrong credentials. Please try again.', icon="🚨")

    def missing_credential_outcome(self):
        """
        Show warning for missing credentials.

        This method displays a warning message when the user fails to provide both username and password.
        """
        st.warning('Please write both username and password')

    def get_controller(self):
        """
        Get the associated controller.

        @return: The controller object associated with this widget.
        """
        return self._controller_aut

    def set_controller(self, controller):
        """
        Set the associated controller.

        @param controller: The new controller object to be associated with this widget.
        """
        self._controller_aut = controller

class LogoutWidget:
    """
    Widget for handling user logout.

    This widget provides functionality for users to log out from the application.
    """

    def __init__(self, controller_log):
        """
        Initialize the LogoutWidget.

        @param controller_log: The controller object for logout operations.
        """
        self._controller_logout = controller_log

    def create(self):
        """
        Create the logout widget.

        This method creates the logout interface with a logout button for users to log out from the application.
        """
        st.sidebar.header('Leave the technician section', divider='grey')
        bottone_logout = st.sidebar.button("Logout")
        if bottone_logout:
            self._controller_logout.operation_logout()

    def positive_logout_outcome(self):
        """
        Show success message for logout.

        This method displays a success message when the logout operation is successful.
        """
        st.success('Logged out', icon="✅")

    def get_controller(self):
        """
        Get the associated controller.

        @return: The controller object associated with this widget.
        """
        return self._controller_logout

    def set_controller(self, controller):
        """
        Set the associated controller.

        @param controller: The new controller object to be associated with this widget.
        """
        self._controller_logout = controller

class SelectWidget:
    """
    Widget for selecting files.

    This widget provides functionality for users to select files from a list of available options.
    """

    def __init__(self, controller_sel):
        """
        Initialize the SelectWidget.

        @param controller_sel: The controller object for file selection operations.
        """
        self.__controller_sel = controller_sel
        self.__file = None

    def create(self):
        """
        Create the file selection widget.

        This method creates the file selection interface with a dropdown menu for selecting files.
        """
        files = self.__controller_sel.operation_get_all_dictionaries()
        file = st.sidebar.selectbox('Your data dictionary files', files, key="dizionari")
        self.__controller_sel.operation_set_current_dictionary(file)
        self.__file = file

    def get_file(self):
        """
        Get the selected file.

        @return: The selected file from the file selection widget.
        """
        return self.__file

class UploadWidget:
    """
    Widget for uploading files.

    This widget provides functionality for users to upload files to the application.
    """

    def __init__(self, controller_up):
        """
        Initialize the UploadWidget.

        @param controller_up: The controller object for file upload operations.
        """
        self.__controller_up = controller_up
        self.__file_uploaded = None
        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 0

    def create(self):
        """
        Create the file upload widget.

        This method creates the file upload interface with a file uploader component for uploading files.
        """
        upload_this_file = st.sidebar.file_uploader("Upload new data dictionary file", accept_multiple_files=False, key = st.session_state["file_uploader_key"])
        st.sidebar.button("Upload file", type="primary", on_click = lambda:self.__operazione_upload(upload_this_file), disabled = upload_this_file is None)

    def __operazione_upload(self, upload_this_file):
        """
        Perform the file upload operation.

        @param upload_this_file: The file object to be uploaded.
        """
        self.__file_uploaded = upload_this_file
        self.__controller_up.operation_update_file_data()

    def get_file_uploaded(self):
        """
        Get the uploaded file.

        @return: The uploaded file from the file upload widget.
        """
        return self.__file_uploaded

    def positive_upload_outcome(self, uploaded_file_name):
        """
        Show success message for file upload.

        This method displays a success message when a file is successfully uploaded.
        
        @param uploaded_file_name: The name of the uploaded file.
        """
        st.success(f'Dictionary "{uploaded_file_name}" uploaded.', icon="✅")
        st.session_state["file_uploader_key"] += 1

    def negative_upload_outcome(self, dictionary_upload_error):
        """
        Show error message for file upload.

        This method displays an error message when a file upload operation fails.

        @param dictionary_upload_error: The error message related to the file upload operation.
        """
        st.error(dictionary_upload_error, icon="🚨")
        st.session_state["file_uploader_key"] += 1

class DeleteWidget:
    """
    Widget for deleting files.

    This widget provides functionality for users to delete files from the application.
    """

    def __init__(self, selection_widget, controller_del):
        """
        Initialize the DeleteWidget.

        @param selection_widget: The file selection widget associated with this deletion widget.
        @param controller_del: The controller object for file deletion operations.
        """
        self._selection_widget = selection_widget
        self._controller_del = controller_del

    def create(self):
        """
        Create the file deletion widget.

        This method creates the file deletion interface with options to select and delete files.
        """
        self._selection_widget.create()
        delete_file_name = self._selection_widget.get_file()
        click_select_file = st.sidebar.button("Delete selected file", type="primary", disabled = delete_file_name is None)
        if click_select_file:
            self._controller_del.operation_delete(delete_file_name)

    def positive_delete_outcome(self, deleted_file_name):
        """
        Show success message for file deletion.

        This method displays a success message when a file is successfully deleted.

        @param deleted_file_name: The name of the deleted file.
        """
        st.success(f'Dictionary "{deleted_file_name}" deleted successfully.', icon="✅")

    def negative_delete_outcome(self, file_name):
        """
        Show error message for file deletion.

        This method displays an error message when a file deletion operation fails.

        @param file_name: The name of the file for which deletion failed.
        """
        st.error(f'Deletion of dictionary "{file_name}" failed.', icon="🚨")

    def get_controller(self):
        """
        Get the associated controller.

        @return: The controller object associated with this widget.
        """
        return self._controller_del

    def set_controller(self, controller):
        """
        Set the associated controller.

        @param controller: The new controller object to be associated with this widget.
        """
        self._controller_del = controller

class ChatWidget:
    """
    Widget for handling chat interactions.

    This widget provides functionality for users to interact with a chat interface.
    """

    def __init__(self, controller_cha):
        """
        Initialize the ChatWidget.

        @param controller_cha: The controller object for chat operations.
        """
        self._controller_chat = controller_cha
        self._user_input = None
        self._current_dictionary = None

    def create(self):
        """
        Create the chat widget.

        This method creates the chat interface where users can input queries and receive responses.
        """
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        for message in st.session_state.chat:
            with st.chat_message(message["role"]):
                st.code(message["content"], language="markdown")
        if self._controller_chat.operation_get_all_dictionaries() == []:
            st.chat_input("A data dictionary has not been uploaded. Please log in as a technician to upload one.", disabled=True)
        else:
            self._user_input = st.chat_input("Type your query here", max_chars=500)
            if self._user_input:
                st.write(f"User has sent the following prompt: {self._user_input}")
                self._controller_chat.operation_generate_response(self._user_input)

    def show_response(self, gen_response):
        """
        Show the generated response in the chat.

        This method displays the response generated for the user query in the chat interface.

        @param gen_response: The generated response to be displayed.
        """
        st.session_state.chat.append({"role": "user", "content": gen_response})
        st.code(f"Response: {gen_response}", language="markdown")

    def get_controller(self):
        """
        Get the associated controller.

        @return: The controller object associated with this widget.
        """
        return self._controller_chat

    def set_controller(self, controller):
        """
        Set the associated controller.

        @param controller: The new controller object to be associated with this widget.
        """
        self._controller_chat = controller
