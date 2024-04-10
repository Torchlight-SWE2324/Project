import os
import shutil
import sys
from streamlit.testing.v1 import AppTest
sys.path.append('ChatSQL')  # Assicurati di aggiungere il percorso che contiene la directory 'embedder'

from embedder import Embedder
from model import JsonSchemaVerifierService, UploadService

def setup_function():
    source_folder = "ChatSQL/test/utils"
    destination_folder = "ChatSQL/database"
    json_filename1 = "swe_music.json"
    json_filename2 = "fitness_app.json"
    source_file_path1 = os.path.join(source_folder, json_filename1)
    source_file_path2 = os.path.join(source_folder, json_filename2)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    destination_file_path = os.path.join(destination_folder, json_filename1)
    destination_file_path2 = os.path.join(destination_folder, json_filename2)
    shutil.copyfile(source_file_path1, destination_file_path)
    shutil.copyfile(source_file_path2, destination_file_path2)
    emb = Embedder()
    json_verifier = JsonSchemaVerifierService()
    upload_service = UploadService(emb, json_verifier)
    uploaded_file_path = "ChatSQL/database/swe_music.json"
    with open(uploaded_file_path, 'r') as file:
        uploaded_file_content = file.read()
    upload_service.upload_dictionary("swe_music.json", uploaded_file_content)


def login_func():
    """
    The function builds an application which has in its GUI only the graphical components of "LoginWidget" 
    and "AuthenticationController" and "AuthenticationService" classes in the back-end
    """
    import streamlit as st
    from model import AuthenticationService
    from controller import AuthenticationController
    from widgets import LoginWidget

    aut_model = AuthenticationService()
    aut_controller = AuthenticationController(aut_model, None)
    login_widget = LoginWidget(aut_controller)
    aut_controller.set_view(login_widget)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "doing_test" not in st.session_state:
        st.session_state.doing_test = True
    aut_model.set_logged_status(False)
    login_widget.create()

def logout_func():
    import streamlit as st
    from model import AuthenticationService
    from controller import LogoutController
    from widgets import LogoutWidget
    aut_model = AuthenticationService()
    log_controller = LogoutController(aut_model, None)
    logout_widget = LogoutWidget(log_controller)
    log_controller.set_view(logout_widget)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = True
        
    if "doing_test" not in st.session_state:
        st.session_state.doing_test = True
    
    aut_model.set_logged_status(True)
    logout_widget.create()

def delete_func():
    from model import DeleteService, SelectionService
    from controller import DeleteController, SelectionController
    from widgets import DeleteWidget, SelectWidget
    del_model = DeleteService()
    sel_model = SelectionService()
    del_controller = DeleteController(del_model, None)
    sel_controller = SelectionController(sel_model, None)
    select_widget = SelectWidget(sel_controller)
    delete_widget = DeleteWidget(select_widget, del_controller)
    del_controller.set_view(delete_widget)
    delete_widget.create()

def chat_func():
    import streamlit as st
    from model import SelectionService, UserResponse, TechnicianResponse, AuthenticationService, ChatService
    from controller import ChatController
    from widgets import ChatWidget
    from embedder import Embedder

    embedder = Embedder()
    user_response = UserResponse(embedder)
    technician_response = TechnicianResponse(embedder)
    cha_model = ChatService(user_response, technician_response)
    aut_model = AuthenticationService()
    sel_model = SelectionService()
    cha_controller = ChatController(cha_model, sel_model, aut_model, None)
    chat_widget = ChatWidget(cha_controller)
    cha_controller.set_view(chat_widget)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    #aut_model.set_logged_status(False)
    if "chat" not in st.session_state:
        st.session_state.chat = []
    chat_widget.create()

def upload_func():
    import streamlit as st
    from model import UploadService
    from controller import UploadController
    from widgets import UploadWidget
    from embedder import Embedder

    embedder = Embedder()
    dictionary_schema_verifier = JsonSchemaVerifierService()
    up_model = UploadService(embedder, dictionary_schema_verifier)
    up_controller = UploadController(up_model, None)
    upload_widget = UploadWidget(up_controller)
    up_controller.set_view(upload_widget)
    # Inizializza il widget di upload
    widget = UploadWidget(up_controller)  # Passa il controller appropriato se necessario
    widget.create()

def test_login_missing_credentials():
    """
    tests the case of trying logging in without inserting both username and password
    """
    at = AppTest.from_function(login_func)
    at.run()

    at.sidebar.text_input[0].set_value("a").run()
    at.sidebar.text_input[1].set_value("").run()
    at.sidebar.button[0].click().run()

    # assert at.sidebar.text_input[0].value == "a"
    # assert at.sidebar.text_input[1].value == "a"
    assert at.session_state.logged_in == False
    assert at.toast[0].value == ":orange[Please write both username and password]" and at.toast[0].icon == "⚠️"

    # assert at.sidebar.button[0].value == False
    # at.sidebar.button[0].click().run()
    # assert at.sidebar.button[0].value == True

def test_login_wrong_credentials():
    """
    tests the case of trying logging in with wrong credentials
    """
    at = AppTest.from_function(login_func)
    at.run()

    at.sidebar.text_input[0].set_value("wrong username").run()
    at.sidebar.text_input[1].set_value("wrong password").run()
    at.sidebar.button[0].click().run()

    assert at.session_state.logged_in == False
    assert at.toast[0].value == ":red[Wrong credentials. Please try again.]" and at.toast[0].icon == "🚨"

def test_login_correct_credentials():
    """
    tests the case of trying logging in with correct credentials
    """
    at = AppTest.from_function(login_func)
    at.run()

    at.sidebar.text_input[0].set_value("admin").run()
    at.sidebar.text_input[1].set_value("admin").run()
    at.sidebar.button[0].click().run()

    assert at.session_state.logged_in == True
    assert at.toast[0].value == ":green[Login successful!]" and at.toast[0].icon == "✅"

def test_logout():
    at = AppTest.from_function(logout_func)
    at.run()

    at.sidebar.button[0].click().run()
    assert at.toast[0].value == ":green[Logged out.]" and at.toast[0].icon == "✅"

def test_delete_true():
    at = AppTest.from_function(delete_func)
    at.run()

    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    at.sidebar.button[0].click().run()
    assert at.toast[0].value == ":green[Dictionary \"swe_music.json\" deleted successfully.]" and at.toast[0].icon == "🗑️"

def test_delete_false():
    at = AppTest.from_function(delete_func)
    at.run()

    at.sidebar.selectbox[0].set_value("fitness_app.json").run()
    at.sidebar.button[0].click().run()
    assert at.toast[0].value == ":red[Deletion of dictionary \"fitness_app.json\" failed.]" and at.toast[0].icon == "🚨"


def test_chat():
    at = AppTest.from_function(chat_func)
    at.run()
    
    at.chat_input[0].set_value("a").run()
    #assert at.text_input[0].value == "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query."
    assert at.chat_message[0].markdown[0].value == "a"
    #assert at.code[0].value != "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query."
    


def test_logout():
    at = AppTest.from_function(logout_func)
    at.run()

    at.sidebar.button[0].click().run()
    assert at.toast[0].value == ":green[Logged out.]" and at.toast[0].icon == "✅"

def test_delete_true():
    at = AppTest.from_function(delete_func)
    at.run()

    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    at.sidebar.button[0].click().run()
    assert at.toast[0].value == ":green[Dictionary \"swe_music.json\" deleted successfully.]" and at.toast[0].icon == "🗑️"

def test_delete_false():
    at = AppTest.from_function(delete_func)
    at.run()

    at.sidebar.selectbox[0].set_value("fitness_app.json").run()
    at.sidebar.button[0].click().run()
    assert at.toast[0].value == ":red[Deletion of dictionary \"fitness_app.json\" failed.]" and at.toast[0].icon == "🚨"


def test_chat():
    at = AppTest.from_function(chat_func)
    at.run()
    
    at.chat_input[0].set_value("a").run()
    #assert at.text_input[0].value == "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query."
    assert at.chat_message[0].markdown[0].value == "a"
    #assert at.code[0].value != "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query."
    


#-------------------------------------------------------------------------------------------------------------------------------------
# test d'integrazione Logout
#-------------------------------------------------------------------------------------------------------------------------------------

def logout_func():
    import streamlit as st
    from model import AuthenticationService
    from controller import LogoutController
    from widgets import LogoutWidget

    aut_model = AuthenticationService()
    log_controller = LogoutController(aut_model, None)
    logout_widget = LogoutWidget(log_controller)
    log_controller.set_view(logout_widget)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = True
    if "doing_test" not in st.session_state:
        st.session_state.doing_test = True
    aut_model.set_logged_status(True)
    logout_widget.create()

def test_logout_correct():
    """
    tests the case of logging out
    """
    at = AppTest.from_function(logout_func)
    at.run()

    at.sidebar.button[0].click().run()
    assert at.session_state.logged_in == False
    assert at.toast[0].value == ":green[Logged out.]" and at.toast[0].icon == "✅"