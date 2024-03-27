import csv
import os

from ResponseGenerator import *
class ModelAuthentication:
    def __init__(self):
        self.utenteloggato = False

    def check_login(self, username, password):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dirPath, "pswrd.csv")
        with open(file_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == username and row[1] == password:
                        self.utenteloggato = True
                        return True
        return False
    
    def logout(self):
        utenteloggato = False
        return utenteloggato
    
    def setUtenteLoggato(self, esito):
        self.utenteloggato = esito

    def getUtenteLoggato(self):
        return self.utenteloggato
    
    
class ModelSelezione:

    def filesInDB(self):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        database_path = os.path.join(dirPath, "database")
        files = os.listdir(database_path)
        return files
    
class ModelUpload:
    def __init__(self):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        self.database_path = os.path.join(dirPath, "database")
        
    def uploadFileModel(self, file):
        if file:
            file_contents = file.getvalue()
            file_path = os.path.join(self.database_path, file.name)  # Use file.name instead of file.path
            with open(file_path, "wb") as f:
                f.write(file_contents)
            return True
        else:
            return False
    
class ModelDelete:
    def __init__(self):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        self.database_path = os.path.join(dirPath, "database")
        self.file_deleted = False
        
    def deleteFile(self, file):
        if file:
            file_paths_to_try = [os.path.join(self.database_path, file)]
            self.file_deleted = False
            for file_path in file_paths_to_try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.file_deleted = True
    
    def getFileDeleted(self):
        return self.file_deleted
    
    def getEsitoFileEliminato(self):
        return self.file_deleted
    
class ModelChat:
    def __init__(self):
        self.response = ""

    def generatePrompt(self, user_input):

        self.response = "Generazione prompt"
        
        # emb = embedderFactory()       //crea l'embedder con l'indice corrente dentro
        # dictionary_name = metodo()    //metodo di classe che si occupa di recuperare il dizionario corrente
        #promptGen = ResponseUser()

        #self.response = promptGen.generatePrompt(emb, user_input, dictionary_name)

        
    def generateDebug(self, user_input):

        self.response = "Generazione debug"

        # emb = embedderFactory()       //crea l'embedder con l'indice corrente dentro
        #debugGen = ResponseTechnician()

        #self.response = debugGen.generateDebug(emb, user_input)

    def getResponse(self):
        return self.response
    
    def setResponse(self, new_response):
        self.response = new_response
    

    
