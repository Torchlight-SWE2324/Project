"""
This module defines classes that define various widgets used in a Streamlit application for handling user interactions,
file uploads, deletions, and chat functionalities.
"""
import random
import time
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
        self._username = None
        self._password = None

    def create(self):
        """
        Create the login widget.

        This method creates the login interface with input fields for username and password,
        along with a login button for submitting the credentials.
        """
        st.sidebar.header('Login in the technician section', divider='grey')
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        login_button = st.sidebar.button("Login")
        if login_button:
            self._notify_login_attempt(username, password)

    def _notify_login_attempt(self, username, password):
        """
        Communicates to the associated controller to try the login.

        @param upload_this_file: The string with the user input used to generate the response.
        """
        self._username = username
        self._password = password
        self._controller_aut.operation_login()

    def positive_login_outcome(self):
        """
        Show success message for login.

        This method displays a success message when the login operation is successful.
        """
        st.markdown(
                    """
                    <style>
                        div[data-testid=toastContainer] {
                                padding: 50px 10px 10px 10px;
                                align-items: end;
                                position: sticky; 
                            }
                        
                            div[data-testid=stToast] {
                                padding: 15px 25px 15px 10px;
                                width: 20%;
                            }
                            
                            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                                font-size: 1.3rem;
                                padding: 10px 10px 10px 40px;
                                text-indent: -1.7em;
                            }
                    </style>
                    """, unsafe_allow_html=True)
        st.toast(':green[Login successful!]', icon="✅")
        time.sleep(1)

    def negative_login_outcome(self):
        """
        Show error message for incorrect credentials.

        This method displays an error message when the user enters incorrect credentials during login.
        """
        st.markdown(
                    """
                    <style>
                        div[data-testid=toastContainer] {
                                padding: 50px 10px 10px 10px;
                                align-items: end;
                                position: sticky; 
                            }
                        
                            div[data-testid=stToast] {
                                padding: 15px 25px 15px 10px;
                                width: 30%;
                            }
                            
                            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                                font-size: 1.3rem;
                                padding: 10px 10px 10px 40px;
                                text-indent: -1.7em;
                            }
                    </style>
                    """, unsafe_allow_html=True)
        st.toast(':red[Wrong credentials. Please try again.]', icon="🚨")

    def missing_credential_outcome(self):
        """
        Show warning for missing credentials.

        This method displays a warning message when the user fails to provide both username and password.
        """
        st.markdown(
                    """
                    <style>
                        div[data-testid=toastContainer] {
                                padding: 50px 10px 10px 10px;
                                align-items: end;
                                position: sticky; 
                            }
                        
                            div[data-testid=stToast] {
                                padding: 15px 25px 15px 10px;
                                width: 30%;
                            }
                            
                            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                                font-size: 1.3rem;
                                padding: 10px 10px 10px 40px;
                                text-indent: -1.7em;
                            }
                    </style>
                    """, unsafe_allow_html=True)
        st.toast(':orange[Please write both username and password]', icon="⚠️")

    def get_username(self):
        """
        Get the username inputted by user.

        @return: The string containing the username inputted by user.
        """
        return self._username

    def get_password(self):
        """
        Get the password inputted by user.

        @return: The string containing the password inputted by user.
        """
        return self._password

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
        st.markdown(
                    """
                    <style>
                        div[data-testid=toastContainer] {
                                padding: 50px 10px 10px 10px;
                                align-items: end;
                                position: sticky; 
                            }
                        
                            div[data-testid=stToast] {
                                padding: 15px 25px 15px 10px;
                                width: 20%;
                            }
                            
                            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                                font-size: 1.3rem;
                                padding: 10px 10px 10px 40px;
                                text-indent: -1.7em;
                            }
                    </style>
                    """, unsafe_allow_html=True)
        st.toast(':green[Logged out.]', icon="✅")
        time.sleep(1)

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
        self._controller_sel = controller_sel
        self._file = None

    def create(self):
        """
        Create the file selection widget.

        This method creates the file selection interface with a dropdown menu for selecting files.
        """
        st.sidebar.title("ChatSQL")
        files = self._controller_sel.operation_get_all_dictionaries()
        file = st.sidebar.selectbox('Your data dictionary files', files)
        self._controller_sel.operation_set_current_dictionary(file)
        self._file = file

    def get_file(self):
        """
        Get the selected file.

        @return: The selected file from the file selection widget.
        """
        return self._file

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
        self._controller_up = controller_up
        self._file_uploaded = None
        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 0

    def create(self):
        """
        Create the file upload widget.

        This method creates the file upload interface with a file uploader component.
        """
        upload_this_file = st.sidebar.file_uploader("Upload new data dictionary file", accept_multiple_files=False, key = st.session_state["file_uploader_key"])
        st.sidebar.button("Upload file", type="primary", on_click = lambda:self._operation_upload(upload_this_file), disabled = upload_this_file is None)

    def _operation_upload(self, upload_this_file):
        """
        Perform the file upload operation.

        @param upload_this_file: The file object to be uploaded.
        """
        self._file_uploaded = upload_this_file
        self._controller_up.operation_update_file_data()

    def positive_upload_outcome(self, uploaded_file_name):
        """
        Show success message for file upload.

        This method displays a success message when a file is successfully uploaded.
        
        @param uploaded_file_name: The name of the uploaded file.
        """
        st.markdown(
                    """
                    <style>
                        div[data-testid=toastContainer] {
                                padding: 50px 10px 10px 10px;
                                align-items: end;
                                position: sticky; 
                            }
                        
                            div[data-testid=stToast] {
                                padding: 15px 25px 15px 10px;
                                width: 40%;
                            }
                            
                            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                                font-size: 1.3rem;
                                padding: 10px 10px 10px 40px;
                                text-indent: -1.7em;
                            }
                    </style>
                    """, unsafe_allow_html=True)
        st.toast(f':green[Dictionary "{uploaded_file_name}" uploaded.]', icon="✅")
        st.session_state["file_uploader_key"] += 1

    def negative_upload_outcome(self, dictionary_upload_error):
        """
        Show error message for file upload.

        This method displays an error message when a file upload operation fails.

        @param dictionary_upload_error: The error message related to the file upload operation.
        """
        st.markdown(
                    """
                    <style>
                        div[data-testid=toastContainer] {
                                padding: 50px 10px 10px 10px;
                                align-items: end;
                                position: sticky; 
                            }
                        
                            div[data-testid=stToast] {
                                padding: 15px 25px 15px 10px;
                                width: 30%;
                            }
                            
                            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                                font-size: 1.3rem;
                                padding: 10px 10px 10px 40px;
                                text-indent: -1.7em;
                            }
                    </style>
                    """, unsafe_allow_html=True)
        st.toast(f':red[{dictionary_upload_error}]', icon="🚨")
        st.session_state["file_uploader_key"] += 1

    def get_file_uploaded(self):
        """
        Get the uploaded file.

        @return: The uploaded file from the file upload widget.
        """
        return self._file_uploaded

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
        self.__selection_widget = selection_widget
        self.__controller_del = controller_del

    def create(self):
        """
        Create the file deletion widget.

        This method creates the file deletion interface with options to select and delete files.
        """
        self.__selection_widget.create()
        delete_file_name = self.__selection_widget.get_file()
        click_select_file = st.sidebar.button("Delete selected file", type="primary", disabled = delete_file_name is None)
        if click_select_file:
            self.__controller_del.operation_delete(delete_file_name)

    def positive_delete_outcome(self, deleted_file_name):
        """
        Show success message for file deletion.

        This method displays a success message when a file is successfully deleted.

        @param deleted_file_name: The name of the deleted file.
        """
        st.markdown(
                    """
                    <style>
                        div[data-testid=toastContainer] {
                                padding: 50px 10px 10px 10px;
                                align-items: end;
                                position: sticky; 
                            }
                        
                            div[data-testid=stToast] {
                                padding: 15px 25px 15px 10px;
                                width: 40%;
                            }
                            
                            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                                font-size: 1.3rem;
                                padding: 10px 10px 10px 40px;
                                text-indent: -1.7em;
                            }
                    </style>
                    """, unsafe_allow_html=True)
        st.toast(f':green[Dictionary "{deleted_file_name}" deleted successfully.]', icon="🗑️")
        time.sleep(1)

    def negative_delete_outcome(self, file_name):
        """
        Show error message for file deletion.

        This method displays an error message when a file deletion operation fails.

        @param file_name: The name of the file for which deletion failed.
        """
        st.markdown(
                    """
                    <style>
                        div[data-testid=toastContainer] {
                                padding: 50px 10px 10px 10px;
                                align-items: end;
                                position: sticky; 
                            }
                        
                            div[data-testid=stToast] {
                                padding: 15px 25px 15px 10px;
                                width: 40%;
                            }
                            
                            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                                font-size: 1.3rem;
                                padding: 10px 10px 10px 40px;
                                text-indent: -1.7em;
                            }
                    </style>
                    """, unsafe_allow_html=True)
        st.toast(f':red[Deletion of dictionary "{file_name}" failed.]', icon="🚨")
        time.sleep(1)

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
        self.__controller_chat = controller_cha
        self.__user_input = None 

    def create(self):
        """
        Create the chat widget.

        This method creates the chat interface where users can input queries and receive responses.
        """
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        for message in st.session_state.chat:
            with st.chat_message(message["role"]):
                st.code(message["content"], language="markdown")
        if self.__controller_chat.operation_get_all_dictionaries() == []:
            st.chat_input("A data dictionary has not been uploaded. Please log in as a technician to upload one.", disabled=True)
        else:
            user_input = st.chat_input("Type your query here", key="chat_input", max_chars=800)
            if user_input:
                self._notify_input_user(user_input)

    def _notify_input_user(self, user_input):
        """
        Communicates to the associated controller to start the generation of response operation.

        @param upload_this_file: The string containing user input used to generate the response.
        """
        st.session_state.chat.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        self.__user_input = user_input
        self.__controller_chat.operation_generate_response()

    def show_response(self, gen_response):
        """
        Show the generated response in the chat.

        This method displays the response generated for the user query in the chat interface.

        @param gen_response: The generated response to be displayed.
        """
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        time.sleep(0.5)
        st.session_state.chat.append({"role": "assistant", "content": gen_response})
        with st.chat_message("assistant"):
            #st.code(f"Response: {gen_response}", language="markdown")
            st.write(f"```\nResponse: {gen_response}\n```")
            

    def get_user_input(self):
        """
        Get the user input.

        @return: The string containing user input from chat input widget.
        """
        return self.__user_input
