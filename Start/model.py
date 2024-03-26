import csv
import os


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
    
