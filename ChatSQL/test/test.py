import unittest
import sys
import os
import shutil
sys.path.append('ChatSQL')  # Assicurati di aggiungere il percorso che contiene la directory 'embedder'
from embedder import *
from model import *
from response import *


class TestEmbedder(unittest.TestCase):
    def test_generate_index(self):
        dictionary_file_name = "swe_music.json"
        embedder = Embedder()
        embedder._index_directory = os.path.join(os.path.dirname(__file__), "indexes")
        embedder._database_directory = os.path.join(os.path.dirname(__file__), "database")
        result_string=embedder.generate_index(dictionary_file_name)
        self.assertEqual(result_string, "index_created")

    def test_generate_upsert_commands(self):
        dictionary_path = "ChatSQL/test/database/swe_music.json"
        embedder = Embedder()
        embedder._index_directory = os.path.join(os.path.dirname(__file__), "indexes")
        embedder._database_directory = os.path.join(os.path.dirname(__file__), "database")
        result_list=embedder.generate_upsert_commands(dictionary_path)
        original_list= [{'table_name': 'users', 'table_description': 'Table containing information about users', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each user'}, {'table_name': 'users', 'table_description': 'Table containing information about users', 'field_name': 'username', 'field_type': 'string', 'field_references': None, 'field_description': 'Username of the user'}, {'table_name': 'users', 'table_description': 'Table containing information about users', 'field_name': 'email', 'field_type': 'string', 'field_references': None, 'field_description': 'Email address of the user'}, {'table_name': 
                        'users', 'table_description': 'Table containing information about users', 'field_name': 'registration_date', 'field_type': 'datetime', 'field_references': None, 'field_description': 'Date and time when the user registered'}, {'table_name': 'artists', 'table_description': 'Table containing information about music artists', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each artist'}, {'table_name': 'artists', 'table_description': 'Table containing information about music artists', 'field_name': 'name', 'field_type': 'string', 'field_references': None, 'field_description': 'Name of the artist'}, {'table_name': 'artists', 'table_description': 'Table containing information about music artists', 'field_name': 'genre', 'field_type': 'string', 'field_references': None, 'field_description': "Genre or category of the artist's music"}, {'table_name': 'albums', 'table_description': 'Table containing information about music albums', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each album'}, {'table_name': 'albums', 'table_description': 'Table containing information about music albums', 'field_name': 'title', 'field_type': 'string', 'field_references': None, 'field_description': 'Title of the album'}, {'table_name': 'albums', 'table_description': 'Table containing information about music albums', 'field_name': 'release_date', 'field_type': 'date', 'field_references': None, 'field_description': 'Date when the album was released'}, {'table_name': 'albums', 'table_description': 'Table containing information about music albums', 'field_name': 'artist_id', 'field_type': 'integer', 'field_references': {'table_name': 'artists', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the artist of the album'}, {'table_name': 'songs', 'table_description': 'Table containing information about individual songs', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each song'}, {'table_name': 'songs', 'table_description': 'Table containing information about individual songs', 'field_name': 'title', 'field_type': 'string', 'field_references': None, 'field_description': 'Title of the song'}, {'table_name': 'songs', 'table_description': 'Table containing information about individual songs', 'field_name': 'duration', 'field_type': 'integer', 'field_references': None, 'field_description': 'Duration of the song in seconds'}, {'table_name': 'songs', 'table_description': 'Table containing information about individual songs', 'field_name': 'album_id', 'field_type': 'integer', 'field_references': {'table_name': 'albums', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the album to which the song belongs'}, {'table_name': 'playlists', 'table_description': 'Table containing information about user-created playlists', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each playlist'}, {'table_name': 'playlists', 'table_description': 'Table containing information about user-created playlists', 'field_name': 'title', 'field_type': 'string', 'field_references': None, 'field_description': 'Title of the playlist'}, {'table_name': 'playlists', 'table_description': 'Table containing information about user-created playlists', 'field_name': 'user_id', 'field_type': 'integer', 'field_references': {'table_name': 'users', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the user who created the playlist'}, {'table_name': 'playlist_songs', 'table_description': 'Table containing information about songs within playlists', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each playlist song entry'}, {'table_name': 'playlist_songs', 'table_description': 'Table containing information about songs within playlists', 'field_name': 'playlist_id', 'field_type': 'integer', 'field_references': {'table_name': 'playlists', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the playlist to which the song belongs'}, {'table_name': 'playlist_songs', 'table_description': 'Table containing information about songs within playlists', 'field_name': 'song_id', 'field_type': 'integer', 'field_references': {'table_name': 'songs', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the song in the playlist'}, {'table_name': 'user_follows_artist', 'table_description': 'Table containing information about users following artists', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each user follows artist entry'}, {'table_name': 'user_follows_artist', 'table_description': 'Table containing information about users following artists', 'field_name': 'user_id', 'field_type': 'integer', 'field_references': {'table_name': 'users', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the user who follows the artist'}, {'table_name': 'user_follows_artist', 'table_description': 'Table containing information about users following artists', 'field_name': 'artist_id', 'field_type': 'integer', 'field_references': {'table_name': 'artists', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the artist being followed'}, {'table_name': 'user_likes_song', 'table_description': 'Table containing information about user likes for songs', 'field_name': 'id', 'field_type': 'integer', 'field_references': None, 'field_description': 'Unique identifier assigned to each user likes song entry'}, {'table_name': 'user_likes_song', 'table_description': 'Table containing information about user likes for songs', 'field_name': 'user_id', 'field_type': 'integer', 'field_references': {'table_name': 'users', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the user who likes the song'}, {'table_name': 'user_likes_song', 'table_description': 'Table containing information about user likes for songs', 'field_name': 'song_id', 'field_type': 'integer', 'field_references': {'table_name': 'songs', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the liked song'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'id', 'field_type': 'integer', 'field_references': 
                        None, 'field_description': 'Unique identifier assigned to each user reviews album entry'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'user_id', 'field_type': 'integer', 'field_references': {'table_name': 'users', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the user who wrote the review'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'album_id', 'field_type': 'integer', 'field_references': {'table_name': 'albums', 'field_name': 'id'}, 'field_description': 'Foreign key referencing the reviewed album'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'rating', 'field_type': 'integer', 'field_references': None, 'field_description': 'Rating given to the album in the review'}, {'table_name': 'user_reviews_album', 'table_description': 'Table containing information about user reviews for albums', 'field_name': 'comment', 'field_type': 'text', 'field_references': None, 'field_description': 'Comments or feedback provided in the review'}]
        self.assertEqual(result_list, original_list )

class TestModel(unittest.TestCase):
#class JsonSchemaVerifierService    
    def test_GetSchemaFilePath(self):
        json_schema = JsonSchemaVerifierService()
        percorso_relativo = "../ChatSQL/ChatSQL/dicitionary_schemas/json_schema.json"
        expected_path = os.path.abspath(percorso_relativo)
        actual_path = json_schema._get_schema_file_path()  # Chiamata privata del metodo
        self.assertEqual(actual_path, expected_path)

    def test_check_dictionary_schema(self):
        json_schema_verifier = JsonSchemaVerifierService()
        uploaded_file_path = "ChatSQL/test/database/swe_music.json"
        with open(uploaded_file_path, 'r') as file:
            uploaded_file_content = file.read()
        response_string = json_schema_verifier.check_dictionary_schema(uploaded_file_content)
        self.assertEqual(response_string, "schema_check_success")
#class DeleteService  
    def test_delete_file(self):
        delete_service = DeleteService()
        delete_service._dir_path = os.path.dirname(os.path.realpath(__file__))
        delete_service._database_path = os.path.join(delete_service._dir_path, "database")
        delete_service._indexes_path = os.path.join(delete_service._dir_path, "indexes")
        file = "swe_music.json"
        delete_service.delete_file(file)
        copy_json()
        self.assertEqual(delete_service._was_file_deleted, True)
         
    def test_get_elimination_outcome(self):
        delete_service = DeleteService()
        self.assertEqual(delete_service._was_file_deleted, delete_service.get_elimination_outcome())

#class AuthenticationService

    def test_check_login(self):
        username = "admin"
        password = "admin"
        authenticationService = AuthenticationService()
        self.assertEqual(authenticationService.check_login(username, password), True)

    def test_set_logged_status(self):
        obj = AuthenticationService()  # Creo un'istanza della tua classe
        obj.set_logged_status(True)  # Imposto lo stato del login a True
        self.assertTrue(obj._is_technician_logged)  # Verifico che lo stato del login sia stato impostato correttamente a True

        obj.set_logged_status(False)  # Imposto lo stato del login a False
        self.assertFalse(obj._is_technician_logged)  # Verifico che lo stato del login sia stato impostato correttamente a False

    def test_get_logged_status(self):
        obj = AuthenticationService()  # Creo un'istanza della tua classe
        obj.set_logged_status(True)  # Imposto lo stato del login a True
        self.assertTrue(obj.get_logged_status())  # Verifico che il metodo get restituisca True

        obj.set_logged_status(False)  # Imposto lo stato del login a False
        self.assertFalse(obj.get_logged_status())

#class ChatService

    def test_generate_prompt(self):
        # Creare un'istanza di ChatService con gli oggetti di risposta simulati
        emb = Embedder()
        user = UserResponse(emb)
        tec = TechnicianResponse(emb)
        chat_service = ChatService(user, tec)

        # Definire input di esempio
        user_input = "HELLO"
        sanitized_user_input = "HELLO"
        dictionary_name = "swe_music.json"

        # Chiamare il metodo generate_prompt
        chat_service.generate_prompt(user_input, sanitized_user_input, dictionary_name)

        self.assertNotEqual(chat_service._response, "No relevant information was found regarding your request.") 

    def test_generate_debug(self):
        # Creare un'istanza di ChatService con gli oggetti di risposta simulati
        emb = Embedder()
        user = UserResponse(emb)
        tec = TechnicianResponse(emb)
        chat_service = ChatService(user, tec)

        # Definire input di esempio
        user_input = "HELLO"
        sanitized_user_input = "HELLO"
        dictionary_name = "swe_music.json"

        # Chiamare il metodo generate_prompt
        chat_service.generate_debug(user_input, sanitized_user_input, dictionary_name)
        self.assertNotEqual(chat_service._response, "No relevant information was found regarding your request.") 




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
    
       
 
if __name__ == '__main__':
    unittest.main()