import sys
import os
import shutil
sys.path.append('ChatSQL')  # Assicurati di aggiungere il percorso che contiene la directory 'embedder'
from embedder import *
from model import *
from response import *



def test_generate_index():
    dictionary_file_name = "swe_music.json"
    embedder = Embedder()
    embedder._index_directory = os.path.join(os.path.dirname(__file__), "indexes")
    embedder._database_directory = os.path.join(os.path.dirname(__file__), "database")
    result_string=embedder.generate_index(dictionary_file_name)
    assert result_string == "index_created"

def test_generate_upsert_commands():
    dictionary_path = "ChatSQL/test/database/swe_music.json"
    embedder = Embedder()
    embedder._index_directory = os.path.join(os.path.dirname(__file__), "indexes")
    embedder._database_directory = os.path.join(os.path.dirname(__file__), "database")
    result_list=embedder.generate_upsert_commands(dictionary_path)
    original_list= [{'table_name': 'users', 'table_description': 'Table containing information about users', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each user'}, {'table_name': 'users', 'table_description': 'Table containing information about users', 'field_name': 'username', 'field_type': 'string', 'field_references': None, 'field_description': 'Username of the user'}, {'table_name': 'users', 'table_description': 'Table containing information about users', 'field_name': 'email', 'field_type': 'string', 'field_references': None, 'field_description': 'Email address of the user'}, {'table_name': 
                    'users', 'table_description': 'Table containing information about users', 'field_name': 'registration_date', 'field_type': 'datetime', 'field_references': None, 'field_description': 'Date and time when the user registered'}, {'table_name': 'artists', 'table_description': 'Table containing information about music artists', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each artist'}, {'table_name': 'artists', 'table_description': 'Table containing information about music artists', 'field_name': 'name', 'field_type': 'string', 'field_references': None, 'field_description': 'Name of the artist'}, {'table_name': 'artists', 'table_description': 'Table containing information about music artists', 'field_name': 'genre', 'field_type': 'string', 'field_references': None, 'field_description': "Genre or category of the artist's music"}, {'table_name': 'albums', 'table_description': 'Table containing information about music albums', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each album'}, {'table_name': 'albums', 'table_description': 'Table containing information about music albums', 'field_name': 'title', 'field_type': 'string', 'field_references': None, 'field_description': 'Title of the album'}, {'table_name': 'albums', 'table_description': 'Table containing information about music albums', 'field_name': 'release_date', 'field_type': 'date', 'field_references': None, 'field_description': 'Date when the album was released'}, {'table_name': 'albums', 'table_description': 'Table containing information about music albums', 'field_name': 'artist_id', 'field_type': 'integer', 'field_references': {'table_name': 'artists', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the artist of the album'}, {'table_name': 'songs', 'table_description': 'Table containing information about individual songs', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each song'}, {'table_name': 'songs', 'table_description': 'Table containing information about individual songs', 'field_name': 'title', 'field_type': 'string', 'field_references': None, 'field_description': 'Title of the song'}, {'table_name': 'songs', 'table_description': 'Table containing information about individual songs', 'field_name': 'duration', 'field_type': 'integer', 'field_references': None, 'field_description': 'Duration of the song in seconds'}, {'table_name': 'songs', 'table_description': 'Table containing information about individual songs', 'field_name': 'album_id', 'field_type': 'integer', 'field_references': {'table_name': 'albums', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the album to which the song belongs'}, {'table_name': 'playlists', 'table_description': 'Table containing information about user-created playlists', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each playlist'}, {'table_name': 'playlists', 'table_description': 'Table containing information about user-created playlists', 'field_name': 'title', 'field_type': 'string', 'field_references': None, 'field_description': 'Title of the playlist'}, {'table_name': 'playlists', 'table_description': 'Table containing information about user-created playlists', 'field_name': 'user_id', 'field_type': 'integer', 'field_references': {'table_name': 'users', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the user who created the playlist'}, {'table_name': 'playlist_songs', 'table_description': 'Table containing information about songs within playlists', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each playlist song entry'}, {'table_name': 'playlist_songs', 'table_description': 'Table containing information about songs within playlists', 'field_name': 'playlist_id', 'field_type': 'integer', 'field_references': {'table_name': 'playlists', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the playlist to which the song belongs'}, {'table_name': 'playlist_songs', 'table_description': 'Table containing information about songs within playlists', 'field_name': 'song_id', 'field_type': 'integer', 'field_references': {'table_name': 'songs', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the song in the playlist'}, {'table_name': 'user_follows_artist', 'table_description': 'Table containing information about users following artists', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each user follows artist entry'}, {'table_name': 'user_follows_artist', 'table_description': 'Table containing information about users following artists', 'field_name': 'user_id', 'field_type': 'integer', 'field_references': {'table_name': 'users', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the user who follows the artist'}, {'table_name': 'user_follows_artist', 'table_description': 'Table containing information about users following artists', 'field_name': 'artist_id', 'field_type': 'integer', 'field_references': {'table_name': 'artists', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the artist being followed'}, {'table_name': 'user_likes_song', 'table_description': 'Table containing information about user likes for songs', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each user likes song entry'}, {'table_name': 'user_likes_song', 'table_description': 'Table containing information about user likes for songs', 'field_name': 'user_id', 'field_type': 'integer', 'field_references': {'table_name': 'users', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the user who likes the song'}, {'table_name': 'user_likes_song', 'table_description': 'Table containing information about user likes for songs', 'field_name': 'song_id', 'field_type': 'integer', 'field_references': {'table_name': 'songs', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the liked song'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'id', 'field_type': 'integer', 'field_references': 
                    None, 'field_description': 'Unique identifier assigned to each user reviews album entry'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'user_id', 'field_type': 'integer', 'field_references': {'table_name': 'users', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the user who wrote the review'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'album_id', 'field_type': 'integer', 'field_references': {'table_name': 'albums', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the reviewed album'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'rating', 'field_type': 'integer', 'field_references': None, 'field_description': 'Rating given to the album in the review'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'comment', 'field_type': 'text', 'field_references': None, 'field_description': 'Comments or feedback provided in the review'}]
    assert result_list == original_list 


#class JsonSchemaVerifierService    
def test_GetSchemaFilePath():
    json_schema = JsonSchemaVerifierService()
    percorso_relativo = "../ChatSQL/ChatSQL/dicitionary_schemas/json_schema.json"
    expected_path = os.path.abspath(percorso_relativo)
    actual_path = json_schema._get_schema_file_path()  
    assert actual_path == expected_path

def test_check_dictionary_schema():
    json_schema_verifier = JsonSchemaVerifierService()
    uploaded_file_path = "ChatSQL/test/database/swe_music.json"
    with open(uploaded_file_path, 'r') as file:
        uploaded_file_content = file.read()
    response_string = json_schema_verifier.check_dictionary_schema(uploaded_file_content)
    assert response_string == "schema_check_success"


def test_check_dictionary_schema_false():
    json_schema_verifier = JsonSchemaVerifierService()
    uploaded_file_path = "ChatSQL/test/database/notCompliantFile.json"
    with open(uploaded_file_path, 'r') as file:
        uploaded_file_content = file.read()
    response_string = json_schema_verifier.check_dictionary_schema(uploaded_file_content)
    assert response_string == "The file is not compliant with the schema. Please upload a valid file."
    

#class DeleteService  
def test_delete_file():
    delete_service = DeleteService()
    delete_service._dir_path = os.path.dirname(os.path.realpath(__file__))
    delete_service._database_path = os.path.join(delete_service._dir_path, "database")
    delete_service._indexes_path = os.path.join(delete_service._dir_path, "indexes")
    file = "swe_music.json"
    delete_service.delete_file(file)
    copy_json()
    assert delete_service._was_file_deleted == True

def test_delete_file_false():
    delete_service = DeleteService()
    delete_service._dir_path = os.path.dirname(os.path.realpath(__file__))
    delete_service._database_path = os.path.join(delete_service._dir_path, "database")
    delete_service._indexes_path = os.path.join(delete_service._dir_path, "indexes")
    file = "file_che_non_esiste.json"
    delete_service.delete_file(file)
    assert delete_service._was_file_deleted == False
        
def test_get_elimination_outcome():
    delete_service = DeleteService()
    assert delete_service._was_file_deleted == delete_service.get_elimination_outcome()

#class AuthenticationService

def test_check_login_true():
    username = "admin"
    password = "admin"
    authenticationService = AuthenticationService()
    assert authenticationService.check_login(username, password) == True

def test_check_login_false():
    username = "admin11"
    password = "admin11"
    authenticationService = AuthenticationService()
    assert authenticationService.check_login(username, password) == False

def test_set_logged_status():
    obj = AuthenticationService()  
    obj.set_logged_status(True)  
    assert obj._is_technician_logged == True 

    obj.set_logged_status(False)  
    assert obj._is_technician_logged == False

def test_get_logged_status():
    obj = AuthenticationService() 
    obj.set_logged_status(True)  
    assert obj.get_logged_status() == True 

    obj.set_logged_status(False) 
    assert obj.get_logged_status() == False

#class ChatService

def test_generate_prompt_false():
    emb = Embedder()
    user = UserResponse(emb)
    tec = TechnicianResponse(emb)
    chat_service = ChatService(user, tec)
    user_input = "HELLO'"
    sanitized_user_input = "HELLO "
    dictionary_name = "swe_music.json"
    chat_service.generate_prompt(user_input, sanitized_user_input, dictionary_name)
    assert chat_service._response == "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query." 

def test_generate_prompt_true():
    emb = Embedder()
    user = UserResponse(emb)
    tec = TechnicianResponse(emb)
    chat_service = ChatService(user, tec)
    user_input = "name"
    sanitized_user_input = "name"
    dictionary_name = "swe_music.json"
    chat_service.generate_prompt(user_input, sanitized_user_input, dictionary_name)
    assert chat_service._response != "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query." 


def test_generate_debug1():
    emb = Embedder()
    user = UserResponse(emb)
    tec = TechnicianResponse(emb)
    chat_service = ChatService(user, tec)
    user_input = "MUSIC'"
    sanitized_user_input = "MUSIC "
    dictionary_name = "swe_music.json"
    chat_service.generate_debug(user_input, sanitized_user_input, dictionary_name)
    assert type(chat_service._response) == str

def test_get_response():
    emb = Embedder()
    user = UserResponse(emb)
    tec = TechnicianResponse(emb)
    chat_service = ChatService(user, tec)
    response_value = "Test response"
    chat_service._response = response_value
    result = chat_service.get_response()
    assert result == response_value

#class UploadService
def test_dictionary_schema_check():
    emb = Embedder()
    json_verifier = JsonSchemaVerifierService()
    upload_service = UploadService(emb, json_verifier)
    uploaded_file_path = "ChatSQL/test/database/swe_music.json"
    with open(uploaded_file_path, 'r') as file:
        uploaded_file_content = file.read()
    result=upload_service._dictionary_schema_check(uploaded_file_content)
    assert result == "schema_check_success"

def test_dictionary_schema_check_false():
    emb = Embedder()
    json_verifier = JsonSchemaVerifierService()
    upload_service = UploadService(emb, json_verifier)
    uploaded_file_path = "ChatSQL/test/database/notCompliantFile.json"
    with open(uploaded_file_path, 'r') as file:
        uploaded_file_content = file.read()
    result=upload_service._dictionary_schema_check(uploaded_file_content)
    assert result == "The file is not compliant with the schema. Please upload a valid file."

def test_get_dictionaries_folder_path():
    emb = Embedder()
    json_verifier = JsonSchemaVerifierService()
    upload_service = UploadService(emb, json_verifier)
    actual_path = upload_service._get_dictionaries_folder_path()
    expected_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
    actual_path_lower = actual_path.lower()
    expected_path_lower = expected_path.lower()
    assert actual_path_lower == expected_path_lower


def test_upload_dictionary():
    emb = Embedder()
    json_verifier = JsonSchemaVerifierService()
    upload_service = UploadService(emb, json_verifier)
    uploaded_file_path = "ChatSQL/database/fitness_app.json"
    with open(uploaded_file_path, 'r') as file:
        uploaded_file_content = file.read()
    result = upload_service.upload_dictionary("fitness_app.json", uploaded_file_content)
    assert result == 'upload_success'

def test_get_all_dictionaries_names():
    emb = Embedder()
    json_verifier = JsonSchemaVerifierService()
    upload_service = UploadService(emb, json_verifier)
    result=upload_service.get_all_dictionaries_names()
    database_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
    files = os.listdir(database_folder_path)
    assert result == files


def test_get_loaded_dictionaries_number():
    emb = Embedder()
    json_verifier = JsonSchemaVerifierService()
    upload_service = UploadService(emb, json_verifier)
    result=upload_service.get_all_dictionaries_names()
    database_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
    files = os.listdir(database_folder_path)
    assert len(result) == len(files)
    
#class SelectionService
def test_get_dictionaries_folder_path_sel_service():
    selection_service = SelectionService()
    actual_path = selection_service._get_dictionaries_folder_path()
    expected_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
    expected_path_lower = expected_path.lower()
    actual_path_lower = actual_path.lower()
    assert actual_path_lower == expected_path_lower
    
def test_get_files_in_db():
    selection_service = SelectionService()
    result = selection_service.get_files_in_db()
    database_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database"))
    files = os.listdir(database_folder_path)
    assert sorted(result) == sorted(files)


def test_set_current_dictionary():
    selection_service = SelectionService()
    current_dictionary_name = "swe_music"
    selection_service.set_current_dictionary(current_dictionary_name)
    retrieved_dictionary_name = selection_service.get_current_dictionary()
    assert retrieved_dictionary_name == current_dictionary_name

def test_get_current_dictionary():
    selection_service = SelectionService()
    current_dictionary_name = "swe_music"
    selection_service.set_current_dictionary(current_dictionary_name)
    retrieved_dictionary_name = selection_service.get_current_dictionary()
    assert retrieved_dictionary_name == current_dictionary_name

#class UserResponse
def test_generate_prompt_false1():
    emb = Embedder()
    user = UserResponse(emb)
    user_query = "awsd"
    sanitized_user_input = "awsd"
    dictionary_name = "swe_music.json"
    prompt = user.generate_prompt(user_query, sanitized_user_input, dictionary_name)
    assert prompt == "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query."
    

def test_generate_prompt_true1():
    emb = Embedder()
    user = UserResponse(emb)
    user_query = "name"
    sanitized_user_input = "name"
    dictionary_name = "swe_music.json"
    prompt = user.generate_prompt(user_query, sanitized_user_input, dictionary_name)
    assert prompt != "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query."
    
#class TechnicianResponse

def test_generate_debug():
    emb = Embedder()
    user = TechnicianResponse(emb)
    user_query = "song"
    sanitized_user_input = "song"
    dictionary_name = "swe_music.json"
    prompt = user.generate_debug(user_query, sanitized_user_input, dictionary_name)
    assert type(prompt) == str


def copy_json():
    source_folder = "ChatSQL/test/utils"
    destination_folder = "ChatSQL/test/database"
    json_filename = "swe_music.json"
    source_file_path = os.path.join(source_folder, json_filename)
    if not os.path.isfile(source_file_path):
        print(f"Source JSON file '{json_filename}' not found in '{source_folder}'")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    destination_file_path = os.path.join(destination_folder, json_filename)
    shutil.copyfile(source_file_path, destination_file_path)

def initt():
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

       
 
if __name__ == '__main__':
    initt()
    