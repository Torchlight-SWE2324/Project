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

#-------------------------------------------------------------------------------------------------------------------------------------
# test d'integrazione login
#-------------------------------------------------------------------------------------------------------------------------------------

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


def test_login_missing_credentials_TS02():
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

def test_login_wrong_credentials_TS02():
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

def test_login_correct_credentials_TS01():
    """
    tests the case of trying logging in with correct credentials
    """
    at = AppTest.from_function(login_func)
    at.run()

    at.sidebar.text_input[0].set_value("admin").run()
    at.sidebar.text_input[1].set_value("admin").run()
    at.sidebar.button[0].click().run()
    assert at.text_input[0].value == "admin" # username
    assert at.text_input[1].value == "admin" # password
    assert at.session_state.logged_in == True
    assert at.toast[0].value == ":green[Login successful!]" and at.toast[0].icon == "✅"

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

def test_logout_correct_TS03():
    """
    tests the case of logging out
    """
    at = AppTest.from_function(logout_func)
    at.run()

    at.sidebar.button[0].click().run()
    assert at.session_state.logged_in == False
    assert at.toast[0].value == ":green[Logged out.]" and at.toast[0].icon == "✅"

#-------------------------------------------------------------------------------------------------------------------------------------
# test d'integrazione delete dizionari
#-------------------------------------------------------------------------------------------------------------------------------------
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


def test_delete_true():
    """
    tests the case of succesfully deleting a dictinary with relative success message
    """
    at = AppTest.from_function(delete_func)
    at.run()

    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    at.sidebar.button[0].click().run()
    assert at.toast[0].value == ":green[Dictionary \"swe_music.json\" deleted successfully.]" and at.toast[0].icon == "🗑️"

def test_delete_false():
    """
    tests the case of not being able to delete a dictinary with relative error message
    """
    at = AppTest.from_function(delete_func)
    at.run()

    at.sidebar.selectbox[0].set_value("fitness_app.json").run()
    at.sidebar.button[0].click().run()
    assert at.toast[0].value == ":red[Deletion of dictionary \"fitness_app.json\" failed.]" and at.toast[0].icon == "🚨"

#-------------------------------------------------------------------------------------------------------------------------------------
# test d'integrazione chat lato utente 
#-------------------------------------------------------------------------------------------------------------------------------------
def chat_prompt_func():
    import streamlit as st
    from model import AuthenticationService, SelectionService, ChatService, UserResponse, TechnicianResponse
    from controller import SelectionController, ChatController
    from widgets import SelectWidget, ChatWidget, st
    from embedder import Embedder

    embedder = Embedder()
    user_response = UserResponse(embedder)
    technician_response = TechnicianResponse(embedder)
    #modelli
    aut_model = AuthenticationService()
    sel_model = SelectionService()
    cha_model = ChatService(user_response, technician_response)
    #controller
    sel_controller = SelectionController(sel_model, None)
    cha_controller = ChatController(cha_model, sel_model, aut_model, None)
    #view
    select_widget = SelectWidget(sel_controller)
    chat_widget = ChatWidget(cha_controller)
    #controller imposto view
    sel_controller.set_view(select_widget)
    cha_controller.set_view(chat_widget)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "doing_test" not in st.session_state:
        st.session_state.doing_test = True
    aut_model.set_logged_status(False)
    select_widget.create()
    chat_widget.create()

def test_chat_prompt_no_similarity():
    """
    tests the case of visualizing both messages of user input and no similarity prompt
    """
    at = AppTest.from_function(chat_prompt_func, default_timeout=30)
    at.run()
    
    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    #assert at.selectbox[0].options == ["swe_music.json","fitness_app.json"]
    at.chat_input[0].set_value("a").run()

    assert at.chat_message[0].avatar == "user"
    assert at.chat_message[0].markdown[0].value == "a"
    assert at.chat_message[1].avatar == "assistant"
    assert at.chat_message[1].markdown[0].value == "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"
    
def test_chat_prompt_with_similarity():
    """
    tests the case of visualizing both messages of user input and prompt with similarities
    """
    at = AppTest.from_function(chat_prompt_func, default_timeout=30)
    at.run()
    
    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    #assert at.selectbox[0].options == ["swe_music.json","fitness_app.json"]
    at.chat_input[0].set_value("All the songs of a certain singer").run()

    assert at.chat_message[0].avatar == "user"
    assert at.chat_message[0].markdown[0].value == "All the songs of a certain singer"
    assert at.chat_message[1].avatar == "assistant"
    assert at.chat_message[1].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"

#-------------------------------------------------------------------------------------------------------------------------------------
# test d'integrazione chat lato tecnico 
#-------------------------------------------------------------------------------------------------------------------------------------
def chat_debug_func():
    import streamlit as st
    from model import AuthenticationService, SelectionService, ChatService, UserResponse, TechnicianResponse
    from controller import SelectionController, ChatController
    from widgets import SelectWidget, ChatWidget, st
    from embedder import Embedder

    embedder = Embedder()
    user_response = UserResponse(embedder)
    technician_response = TechnicianResponse(embedder)
    #modelli
    aut_model = AuthenticationService()
    sel_model = SelectionService()
    cha_model = ChatService(user_response, technician_response)
    #controller
    sel_controller = SelectionController(sel_model, None)
    cha_controller = ChatController(cha_model, sel_model, aut_model, None)
    #view
    select_widget = SelectWidget(sel_controller)
    chat_widget = ChatWidget(cha_controller)
    #controller imposto view
    sel_controller.set_view(select_widget)
    cha_controller.set_view(chat_widget)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = True
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "doing_test" not in st.session_state:
        st.session_state.doing_test = True
    aut_model.set_logged_status(True)
    select_widget.create()
    chat_widget.create()

def test_chat_debug():
    """
    tests the case of visualizing both messages of technician input and debug message
    """
    at = AppTest.from_function(chat_debug_func, default_timeout=30)
    at.run()
    
    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    #assert at.selectbox[0].options == ["swe_music.json","fitness_app.json"]
    at.chat_input[0].set_value("All the songs of a certain singer").run()

    assert at.chat_message[0].avatar == "user"
    assert at.chat_message[0].markdown[0].value == "All the songs of a certain singer"
    assert at.chat_message[1].avatar == "assistant"
    assert at.chat_message[1].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"