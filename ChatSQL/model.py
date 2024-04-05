import csv
import os
import shutil

from ResponseGenerator import *
from abc import ABC, abstractmethod
from jsonschema import validate, ValidationError

class DictionarySchemaVerifierService(ABC):
    @abstractmethod
    def checkDictionarySchema(self, uploaded_file_content) -> str: pass

class JsonSchemaVerifierService(DictionarySchemaVerifierService):
    def __get_schema_file_path(self) -> str:
        dictionary_schema_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dicitionary_schemas")
        return os.path.join(dictionary_schema_folder_path, "json_schema.json")

    def checkDictionarySchema(self, uploaded_file_content) -> str:
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
            return f"The file is not compliant with the schema. Please upload a valid file."


class UploadService:
    def __init__(self, embedder, dictionary_schema_verifier):
        self.__dictionary_schema_verifier = dictionary_schema_verifier
        self.__embedder = embedder

    def __dictionarySchemaCheck(self, uploaded_file_content):
        return self.__dictionary_schema_verifier.checkDictionarySchema(uploaded_file_content)

    def __getDictionariesFolderPath(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")

    def uploadDictionary(self, uploaded_file_name, uploaded_file_content) -> str:
        dictionary_check = self.__dictionarySchemaCheck(uploaded_file_content)

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

    def getLoadedDictionariesNumber(self) -> int:
        return len(self.getAllDictionariesNames())

    def getAllDictionariesNames(self):
        dictionary_folder_path = self.__getDictionariesFolderPath()
        list = []
        
        for name in os.listdir(dictionary_folder_path):
            if os.path.isfile(os.path.join(dictionary_folder_path, name)):
                list.append(name)
        return list


class SelectionService:
    def __init__(self):
        self.__current_dictionary = None

    def __getDictionariesFolderPath(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")

    def getFilesInDB(self):
        dictionary_folder_path = self.__getDictionariesFolderPath()
        list = []
        
        for name in os.listdir(dictionary_folder_path):
            if os.path.isfile(os.path.join(dictionary_folder_path, name)):
                list.append(name)
        sorted_list = sorted(list, key=lambda x: os.path.getmtime(os.path.join(dictionary_folder_path, x)), reverse=True)
        return sorted_list

    def setCurrentDictionary(self, dictionary_name):
        self.__current_dictionary = dictionary_name

    def getCurrentDictionary(self):
        return self.__current_dictionary


class DeleteService:
    def __init__(self):
        _dir_path = os.path.dirname(os.path.realpath(__file__))
        self._database_path = os.path.join(_dir_path, "database")
        self._indexes_path = os.path.join(_dir_path, "indexes")
        self._was_file_deleted = False
        
    def deleteFile(self, file):
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
    
    def getEliminationOutcome(self):
        return self._was_file_deleted
    

class ChatService:
    def __init__(self, response_user, response_technician):
        self._response = ""
        #self._model_path = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self._data_path = os.path.join(os.path.dirname(__file__), "indexes")
        self._response_user = response_user
        self._response_technician = response_technician

    def generatePrompt(self, user_input, sanitized_user_input, dictionary_name):
        self._response = self._response_user.generatePrompt(user_input, sanitized_user_input, dictionary_name)

    def generateDebug(self, user_input, sanitized_user_input, dictionary_name):
        self._response =  self._response_technician.generateDebug(user_input, sanitized_user_input, dictionary_name)

    def getResponse(self):
        return self._response
    
    def setResponse(self, new_response):
        self._response = new_response


class AuthenticationService:
    def __init__(self):
        self._is_technician_logged = False

    # used by the controller, sets the status of "self._is_technician_logged" to True and returns True only if inserted credentials(username and password) are correct
    # otherwise returns false
    def checkLogin(self, username, password):
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

    # used by the controller, sets the status of "self._is_technician_logged" to the value of "status" (in this case False)
    def setLoggedStatus(self, status):
        self._is_technician_logged = status

    def getLoggedStatus(self):
        return self._is_technician_logged