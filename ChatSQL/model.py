"""
This module defines the models of the application.
The models are responsible for handling the data and business logic of the application.
"""

import csv
import os
import shutil

from response import *
from abc import ABC, abstractmethod
from jsonschema import validate, ValidationError

class DictionarySchemaVerifierService(ABC):
    """
    This class defines an abstract base class for verifying dictionary schemas.
    """

    @abstractmethod
    def check_dictionary_schema(self, uploaded_file_content) -> str:
        """
        Verify the dictionary schema of the uploaded file content.

        @param uploaded_file_content: Content of the uploaded file.
        @return: String indicating the result of schema verification.
        """
        pass

class JsonSchemaVerifierService(DictionarySchemaVerifierService):
    """
    This class implements a JSON schema verifier based on DictionarySchemaVerifierService.
    """

    def __get_schema_file_path(self) -> str:
        """
        Get the file path of the JSON schema file.

        @return: String representing the file path of the JSON schema.
        """
        dictionary_schema_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dicitionary_schemas")
        return os.path.join(dictionary_schema_folder_path, "json_schema.json")

    def check_dictionary_schema(self, uploaded_file_content) -> str:
        """
        Verify the dictionary schema of the uploaded JSON file content.

        @param uploaded_file_content: Content of the uploaded JSON file.
        @return: String indicating the result of schema verification.
        """
        schema_file_path = self.__get_schema_file_path()

        try:
            with open(schema_file_path, "r") as schema_file:
                dictionary_data, json_schema = json.loads(uploaded_file_content), json.load(schema_file)
        except json.JSONDecodeError as e:
            return f"JSON file could not be loaded. Error: {e}"

        try:
            validate(instance=dictionary_data, schema=json_schema)
            return "schema_check_success"
        except ValidationError as e:
            return "The file is not compliant with the schema. Please upload a valid file."

class UploadService:
    """
    This class handles the uploading of dictionary files.
    """

    def __init__(self, embedder, dictionary_schema_verifier):
        """
        Initialize the UploadService with an embedder and dictionary schema verifier.

        @param embedder: Embedder object for indexing.
        @param dictionary_schema_verifier: Object for verifying dictionary schemas.
        """
        self.__dictionary_schema_verifier = dictionary_schema_verifier
        self.__embedder = embedder

    def _dictionary_schema_check(self, uploaded_file_content):
        """
        Check the dictionary schema of the uploaded file content.

        @param uploaded_file_content: Content of the uploaded file.
        @return: String indicating the result of schema verification.
        """
        return self.__dictionary_schema_verifier.check_dictionary_schema(uploaded_file_content)

    def _get_dictionaries_folder_path(self) -> str:
        """
        Get the folder path where dictionaries are stored.

        @return: String representing the folder path of dictionaries.
        """
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")

    def upload_dictionary(self, uploaded_file_name, uploaded_file_content) -> str:
        """
        Upload a dictionary file after schema verification.

        @param uploaded_file_name: Name of the uploaded file.
        @param uploaded_file_content: Content of the uploaded file.
        @return: String indicating the upload status.
        """
        dictionary_check = self._dictionary_schema_check(uploaded_file_content)

        if dictionary_check == "schema_check_success":
            dictionary_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")
            dictionary_path = os.path.join(dictionary_folder_path, uploaded_file_name)

            with open(dictionary_path, "wb") as destination_file:
                file_content = uploaded_file_content.encode()
                destination_file.write(file_content)

            index_creation_result = self.__embedder.generate_index(uploaded_file_name)
            if index_creation_result == "index_created":
                return 'upload_success'
            else:
                return index_creation_result
        else:
            return dictionary_check

    def get_all_dictionaries_names(self):
        """
        Get the names of all uploaded dictionaries.

        @return: List of strings representing dictionary names.
        """
        dictionary_folder_path = self._get_dictionaries_folder_path()
        dict_list = []
        
        for name in os.listdir(dictionary_folder_path):
            if os.path.isfile(os.path.join(dictionary_folder_path, name)):
                dict_list.append(name)
        return dict_list

    def get_loaded_dictionaries_number(self) -> int:
        """
        Get the number of loaded dictionaries.

        @return: Integer representing the number of loaded dictionaries.
        """
        return len(self.get_all_dictionaries_names())

class SelectionService:
    """
    This class handles selection-related operations.
    """

    def __init__(self):
        """
        Initialize the SelectionService.
        """
        self.__current_dictionary = None

    def _get_dictionaries_folder_path(self) -> str:
        """
        Get the folder path where dictionaries are stored.

        @return: String representing the folder path of dictionaries.
        """
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")

    def get_files_in_db(self):
        """
        Get the list of files in the database.

        @return: List of strings representing file names.
        """
        dictionary_folder_path = self._get_dictionaries_folder_path()
        dict_list = []
        for name in os.listdir(dictionary_folder_path):
            if os.path.isfile(os.path.join(dictionary_folder_path, name)):
                dict_list.append(name)
        sorted_list = sorted(dict_list, key=lambda x: os.path.getmtime(os.path.join(dictionary_folder_path, x)), reverse=True)
        return sorted_list

    def set_current_dictionary(self, dictionary_name):
        """
        Set the current dictionary.

        @param dictionary_name: Name of the dictionary to set as current.
        """
        self.__current_dictionary = dictionary_name

    def get_current_dictionary(self):
        """
        Get the current dictionary.

        @return: Name of the current dictionary.
        """
        return self.__current_dictionary

class DeleteService:
    """
    This class handles deletion of files and associated indexes.
    """

    def __init__(self):
        """
        Initialize the DeleteService.
        """
        _dir_path = os.path.dirname(os.path.realpath(__file__))
        self._database_path = os.path.join(_dir_path, "database")
        self._indexes_path = os.path.join(_dir_path, "indexes")
        self._was_file_deleted = False

    def delete_file(self, file):
        """
        Delete the specified file and its associated indexes.

        @param file: Name of the file to delete.
        """
        was_json_deleted = False
        was_index_deleted = False
        if file:
            file_paths_to_try = [os.path.join(self._database_path, file)]
            self._was_file_deleted = False
            for file_path in file_paths_to_try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    was_json_deleted = True 
            filename_without_extension = os.path.splitext(file)[0]
            indexes_directory = os.path.join(self._indexes_path, filename_without_extension)
            if os.path.isdir(indexes_directory):
                for index_file in os.listdir(indexes_directory):
                    file_path = os.path.join(indexes_directory, index_file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                shutil.rmtree(indexes_directory)
                was_index_deleted = True
        if was_json_deleted and was_index_deleted:
            self._was_file_deleted = True
    
    def get_elimination_outcome(self):
        """
        Get the outcome of the elimination process.

        @return: Boolean indicating if the file was successfully deleted.
        """
        return self._was_file_deleted

class ChatService:
    """
    This class handles chat-related services.
    """

    def __init__(self, response_user, response_technician):
        """
        Initialize the ChatService.

        @param response_user: Response object for user interactions.
        @param response_technician: Response object for technician interactions.
        """
        self._response = ""
        self._data_path = os.path.join(os.path.dirname(__file__), "indexes")
        self._response_user = response_user
        self._response_technician = response_technician

    def generate_prompt(self, user_input, sanitized_user_input, dictionary_name):
        """
        Generate a prompt based on user input.

        @param user_input: User's input.
        @param sanitized_user_input: Sanitized version of user's input.
        @param dictionary_name: Name of the current dictionary.
        """
        self._response = self._response_user.generate_prompt(user_input, sanitized_user_input, dictionary_name)

    def generate_debug(self, user_input, sanitized_user_input, dictionary_name):
        """
        Generate a debug message based on user input.

        @param user_input: User's input.
        @param sanitized_user_input: Sanitized version of user's input.
        @param dictionary_name: Name of the current dictionary.
        """
        self._response =  self._response_technician.generate_debug(user_input, sanitized_user_input, dictionary_name)

    def get_response(self):
        """
        Get the response generated by the service.

        @return: Response string.
        """
        return self._response

class AuthenticationService:
    """
    This class handles user authentication.
    """

    def __init__(self):
        """
        Initialize the AuthenticationService.
        """
        self._is_technician_logged = False

    def check_login(self, username, password):
        """
        Check user login credentials.

        @param username: User's username.
        @param password: User's password.
        @return: Boolean indicating successful login.
        """
        try:
            _dir_path = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(_dir_path, "pswrd.csv")
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == username and row[1] == password:
                        self._is_technician_logged = True
                        return True
        except Exception as e:
            print(f"An error occurred: {e}")
        return False

    def set_logged_status(self, status):
        """
        Set the logged-in status.

        @param status: Boolean status to set.
        """
        self._is_technician_logged = status

    def get_logged_status(self):
        """
        Get the logged-in status.

        @return: Boolean indicating logged-in status.
        """
        return self._is_technician_logged
