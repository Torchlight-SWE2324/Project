import csv
import os
import shutil #per eliminare cartella (è di python)

from uploadServiceTemplate import UploadServiceTemplace
from ResponseGenerator import *
#from embedder import *
#from txtai import Embeddings
from abc import ABC, abstractmethod
from jsonschema import validate, ValidationError

class DictionarySchemaVerifierService(ABC):
    @abstractmethod
    def check_dictionary_schema(self, uploaded_file_name, uploaded_file_content) -> str: pass

class JsonSchemaVerifierService(DictionarySchemaVerifierService):
    def __get_schema_file_path(self) -> str:
        dictionary_schema_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dicitionary_schemas")
        return os.path.join(dictionary_schema_folder_path, "json_schema.json")

    def check_dictionary_schema(self, uploaded_file_name, uploaded_file_content) -> str:
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


class ModelUpload:
    #def __init__(self, dictionary_schema_verifier):
    def __init__(self):
        self.database_path = self.__get_dictionaries_folder_path()
        self.dictionary_schema_verifier = JsonSchemaVerifierService()

    def __dictionary_schema_check(self, uploaded_file_name, uploaded_file_content):
        return self.dictionary_schema_verifier.check_dictionary_schema(uploaded_file_name, uploaded_file_content)

    def __get_dictionaries_folder_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")


    '''    
    def upload_dictionary(self, file):
        if file:
            file_contents = file.getvalue()
            file_path = os.path.join(self.database_path, file.name)  # Use file.name instead of file.path
            with open(file_path, "wb") as f:
                f.write(file_contents)

            emb = UploadServiceTemplace()
            emb.generareIndex(file.name)

            return True
        else:
            return False
    '''
    def upload_dictionary(self, uploaded_file_name, uploaded_file_content):
        dictionary_check = self.__dictionary_schema_check(uploaded_file_name, uploaded_file_content)

        if dictionary_check == "schema_check_success":
            print("if dictionary_check == \"schema_check_success\":")
            dictionary_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")
            dictionary_path = os.path.join(dictionary_folder_path, uploaded_file_name)

            with open(dictionary_path, "wb") as destination_file:
                file_content = uploaded_file_content.encode()
                destination_file.write(file_content)

            emb = UploadServiceTemplace()
            emb.generareIndex(uploaded_file_name)

            return 'upload_success'

        else:
            return dictionary_check

    def get_loaded_dictionaries_number(self) -> int:
        return len(self.get_all_dictionaries_names())

    def get_all_dictionaries_names(self):
        dictionary_folder_path = self.__get_dictionaries_folder_path()
        list = []
        for name in os.listdir(dictionary_folder_path):
            if os.path.isfile(os.path.join(dictionary_folder_path, name)):
                list.append(name)
        return list


class ModelSelezione:
    def __init__(self):
        self.dizionarioAttuale = None

    def __get_dictionaries_folder_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "database")

    def filesInDB(self):
        '''
        dirPath = os.path.dirname(os.path.realpath(__file__))
        database_path = os.path.join(dirPath, "database")
        files = os.listdir(database_path)
        return files
        '''
        dictionary_folder_path = self.__get_dictionaries_folder_path()
        list = []
        for name in os.listdir(dictionary_folder_path):
            if os.path.isfile(os.path.join(dictionary_folder_path, name)):
                list.append(name)
        return list

    def setDizionarioAttuale(self, dictionary_name):
        self.dizionarioAttuale = dictionary_name

    def getDizionarioAttuale(self):
        return self.dizionarioAttuale

class ModelDelete:
    def __init__(self):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        self.database_path = os.path.join(dirPath, "database")
        self.indexes_path = os.path.join(dirPath, "indexes")
        self.file_deleted = False
        
    def deleteFile(self, file):
        json_deleted = False
        index_deleted = False
        print(file)
        if file:
            file_paths_to_try = [os.path.join(self.database_path, file)]
            self.file_deleted = False
            for file_path in file_paths_to_try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    json_deleted = True 

            for index_file in os.listdir(self.indexes_path + "\\" + os.path.splitext(file)[0]):
                file_path = os.path.join(self.indexes_path, os.path.splitext(file)[0], index_file)
                if os.path.isfile(file_path):
                    os.remove(file_path) #per eliminare i file nella cartella
                    #importata per eliminare la cartella
                    shutil.rmtree(os.path.join(self.indexes_path, os.path.splitext(file)[0]))
                    index_deleted = True

        if json_deleted == True and index_deleted == True:
            self.file_deleted = True
    
    def getEsitoFileEliminato(self):
        return self.file_deleted
    
class ModelChat:
    def __init__(self):
        self.response = ""
        self.model_path = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.data_path = os.path.join(os.path.dirname(__file__), "indexes")

    def generatePrompt(self, user_input, dictionary_name):
        promptGen = ResponseUser()
        self.response = promptGen.generatePrompt( user_input, dictionary_name)

    def generateDebug(self, user_input, dictionary_name):
        debugGen = ResponseTechnician()
        self.response = debugGen.generateDebug(user_input, dictionary_name)

    def getResponse(self):
        return self.response
    
    def setResponse(self, new_response):
        self.response = new_response

class ModelAuthentication:
    def __init__(self):
        self.utenteloggato = False

    def check_login(self, username, password):
        try:
            dirPath = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(dirPath, "pswrd.csv")
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == username and row[1] == password:
                        self.utenteloggato = True
                        return True
        except Exception as e:
            print(f"An error occurred: {e}")
        return False

    def logout(self):
        utenteloggato = False
        return utenteloggato

    def setUtenteLoggato(self, esito):
        self.utenteloggato = esito

    def getUtenteLoggato(self):
        return self.utenteloggato