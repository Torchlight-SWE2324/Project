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
    uploaded_file_path = "ChatSQL/database/fitness_app.json"
    with open(uploaded_file_path, 'r') as file:
        uploaded_file_content = file.read()
    upload_service.upload_dictionary("fitness_app.json", uploaded_file_content)

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
    assert at.text_input[0].value == "admin" # username
    assert at.text_input[1].value == "admin" # password
    assert at.session_state.logged_in == True
    assert at.toast[0].value == ":green[Login successful!]" and at.toast[0].icon == "✅"



#-------------------------------------------------------------------------------------------------------------------------------------
# test sistema Logout
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
# test sistema delete dizionari
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

#-------------------------------------------------------------------------------------------------------------------------------------
# test sistema chat lato utente 
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

def test_chat_prompt_no_similarity_TS14():
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
    
def test_chat_prompt_with_similarity_TS13():
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

def test_chat_prompt_differente_languages_TS17():
    """
    tests the case of LLM understanding english, italian, romanian, chinese and russian interrogations
    """
    at = AppTest.from_function(chat_prompt_func, default_timeout=30)
    at.run()
    
    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    at.chat_input[0].set_value("All the songs of a certain singer").run()
    assert at.chat_message[0].markdown[0].value == "All the songs of a certain singer"
    assert at.chat_message[1].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"
    at.chat_input[0].set_value("Tutte le canzoni di un certo cantante").run()
    assert at.chat_message[2].markdown[0].value == "Tutte le canzoni di un certo cantante"
    assert at.chat_message[3].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"
    at.chat_input[0].set_value("Toate melodiile unui anumit cântăreț").run()
    assert at.chat_message[4].markdown[0].value == "Toate melodiile unui anumit cântăreț"
    assert at.chat_message[5].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"
    at.chat_input[0].set_value("某个歌手的所有歌曲").run()
    assert at.chat_message[6].markdown[0].value == "某个歌手的所有歌曲"
    assert at.chat_message[7].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"
    at.chat_input[0].set_value("Все песни определенного певца").run()
    assert at.chat_message[8].markdown[0].value == "Все песни определенного певца"
    assert at.chat_message[9].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"
def test_chat_prompt_similarity_filter_TS19():
    """
    tests the case of filter functionality working properly for the generation of prompt
    """
    at = AppTest.from_function(chat_prompt_func, default_timeout=30)
    at.run()
    
    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    at.chat_input[0].set_value("All the songs of a certain singer").run()

    assert at.chat_message[0].avatar == "user"
    assert at.chat_message[0].markdown[0].value == "All the songs of a certain singer"
    assert at.chat_message[1].avatar == "assistant"
    assert at.chat_message[1].markdown[0].value == "```\nThe database contains the following tables:\n\ntable 'songs' with fields:\n'id' that contains Unique identifier assigned to each song;\n'title' that contains Title of the song;\n'duration' that contains Duration of the song in seconds;\n'album_id' that contains Foreign key referencing the album to which the song belongs;\n\ntable 'playlist_songs' with fields:\n'id' that contains Unique identifier assigned to each playlist song entry;\n'playlist_id' that contains Foreign key referencing the playlist to which the song belongs;\n'song_id' that contains Foreign key referencing the song in the playlist;\n\ntable 'user_likes_song' with fields:\n'id' that contains Unique identifier assigned to each user likes song entry;\n'user_id' that contains Foreign key referencing the user who likes the song;\n'song_id' that contains Foreign key referencing the liked song;\n\nand the database contains the following relationships:\n'songs.album_id' references albums.id';\n'playlist_songs.playlist_id' references playlists.id';\n'playlist_songs.song_id' references songs.id';\n'user_likes_song.user_id' references users.id';\n'user_likes_song.song_id' references songs.id';\n\nGenerate the SQL query equivalent to: All the songs of a certain singer\n```"
    
def test_chat_input_area_TS10():
    at = AppTest.from_file("../main.py")
    at.run()

    at.chat_input[0].set_value("All the songs of a certain singer")
    assert at.chat_input[0].value == "All the songs of a certain singer"
    at.chat_input[0].set_value("Test the chat input area")
    assert at.chat_input[0].value == "Test the chat input area"


#-------------------------------------------------------------------------------------------------------------------------------------
# test sistema chat lato tecnico 
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

def test_chat_debug_TS15():
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

#-------------------------------------------------------------------------------------------------------------------------------------
# test sistema selezione
#-------------------------------------------------------------------------------------------------------------------------------------
def select_func():
    import streamlit as st
    from model import SelectionService
    from controller import SelectionController
    from widgets import SelectWidget

    #modelli
    sel_model = SelectionService()
    #controller
    sel_controller = SelectionController(sel_model, None)
    #view
    select_widget = SelectWidget(sel_controller)
    #controller imposto view
    sel_controller.set_view(select_widget)
    if "doing_test" not in st.session_state:
        st.session_state.doing_test = True
    select_widget.create()


def test_select_dictionary():
    """
    tests the case of visualizing the selected dictionary name as the value displayed in the selectbox
    """
    at = AppTest.from_function(select_func, default_timeout=3)
    at.run()

    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    assert at.selectbox[0].value == "swe_music.json"
    at.sidebar.selectbox[0].set_value("fitness_app.json").run()
    assert at.selectbox[0].value == "fitness_app.json"

def test_view_dictionary_TS08():
    """
    tests the case of visualizing all the saved dictionaries name in the selectbox
    """
    at = AppTest.from_function(select_func, default_timeout=3)
    at.run()

    assert at.sidebar.selectbox[0].options == ["fitness_app.json","swe_music.json"]

#-------------------------------------------------------------------------------------------------------------------------------------
# test sistema input
#-------------------------------------------------------------------------------------------------------------------------------------
#non svolgibili perché la classe AppTest di Streamlit non supporta ancora il widget file_uploader nella versione 1.30.0 di Streamlit

#-------------------------------------------------------------------------------------------------------------------------------------
# test sistema chat & login
#-------------------------------------------------------------------------------------------------------------------------------------
def login_chat_func():
    """
    The function builds an application which has in its GUI the graphical components of "SelectWidget", "ChatWidget" and "LoginWidget" 
    and their Controllers and Models in the back-end
    """
    import streamlit as st
    from model import AuthenticationService, SelectionService, ChatService, UserResponse, TechnicianResponse
    from controller import AuthenticationController, SelectionController, ChatController
    from widgets import LoginWidget, SelectWidget, ChatWidget
    from embedder import Embedder

    embedder = Embedder()
    user_response = UserResponse(embedder)
    technician_response = TechnicianResponse(embedder)
    aut_model = AuthenticationService()
    sel_model = SelectionService()
    cha_model = ChatService(user_response, technician_response)
    aut_controller = AuthenticationController(aut_model, None)
    sel_controller = SelectionController(sel_model, None)
    cha_controller = ChatController(cha_model, sel_model, aut_model, None)
    login_widget = LoginWidget(aut_controller)
    select_widget = SelectWidget(sel_controller)
    chat_widget = ChatWidget(cha_controller)
    aut_controller.set_view(login_widget)
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
    login_widget.create()



def test_login_chat_TS20():
    """
    tests the case of all chat messages being deleted when login is successfull
    """
    at = AppTest.from_function(login_chat_func, default_timeout=30)
    at.run()

    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    #assert at.selectbox[0].options == ["swe_music.json","fitness_app.json"]
    at.chat_input[0].set_value("All the songs of a certain singer").run()

    assert at.chat_message[0].markdown[0].value == "All the songs of a certain singer"
    assert at.chat_message[1].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"
    
    at.sidebar.text_input[0].set_value("admin").run()
    at.sidebar.text_input[1].set_value("admin").run()
    at.sidebar.button[0].click().run()
    assert at.session_state.logged_in == True
    assert at.toast[0].value == ":green[Login successful!]" and at.toast[0].icon == "✅"

    try:
        assert at.chat_message[0].markdown[0].value == "All the songs of a certain singer"
    except IndexError:
        pass
    else:
        # If no IndexError occurs, the test fails
        assert False, "Expected IndexError did not occur"
    


#-------------------------------------------------------------------------------------------------------------------------------------
# test sistema chat & logout
#-------------------------------------------------------------------------------------------------------------------------------------
def logout_chat_func():
    """
    The function builds an application which has in its GUI only the graphical components of "LoginWidget" 
    and "AuthenticationController" and "AuthenticationService" classes in the back-end
    """
    import streamlit as st
    from model import AuthenticationService, SelectionService, ChatService, UserResponse, TechnicianResponse
    from controller import LogoutController, SelectionController, ChatController
    from widgets import LogoutWidget, SelectWidget, ChatWidget
    from embedder import Embedder

    embedder = Embedder()
    user_response = UserResponse(embedder)
    technician_response = TechnicianResponse(embedder)
    aut_model = AuthenticationService()
    sel_model = SelectionService()
    cha_model = ChatService(user_response, technician_response)
    log_controller = LogoutController(aut_model, None)
    sel_controller = SelectionController(sel_model, None)
    cha_controller = ChatController(cha_model, sel_model, aut_model, None)
    logout_widget = LogoutWidget(log_controller)
    select_widget = SelectWidget(sel_controller)
    chat_widget = ChatWidget(cha_controller)
    log_controller.set_view(logout_widget)
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
    logout_widget.create()
   

def test_logout_chat_TS21():
    """
    tests the case of all chat messages being deleted when logging out from technician area
    """
    at = AppTest.from_function(logout_chat_func, default_timeout=30)
    at.run()

    at.sidebar.selectbox[0].set_value("swe_music.json").run()
    at.chat_input[0].set_value("All the songs of a certain singer").run()

    assert at.chat_message[0].markdown[0].value == "All the songs of a certain singer"
    assert at.chat_message[1].markdown[0].value != "```\nNo relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query.\n```"
    
    at.sidebar.button[0].click().run()
    assert at.session_state.logged_in == False
    assert at.toast[0].value == ":green[Logged out.]" and at.toast[0].icon == "✅"

    try:
        assert at.chat_message[0].markdown[0].value == "All the songs of a certain singer"
    except IndexError:
        pass
    else:
        # If no IndexError occurs, the test fails
        assert False, "Expected IndexError did not occur"

"""
TS8  V
TS10 V
TS11 Non sono riuscito
TS16 non fattibile
TS17 V
TS18 non fattibile
TS19 V
TS20 V
TS21 V
"""