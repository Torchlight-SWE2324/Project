from embedder import *
import os

class UploadServiceTemplace:
    def __init__(self):
        self.emb = Embedder()
        self.embe = self.emb.getEmb()
    
    def generareIndex(self, dictionary_file_name):
        try:
            if not os.path.exists(self.emb.indexDirectory):
                os.makedirs(self.emb.indexDirectory)
            
            commands = self.emb.generateUpsertCommands(os.path.join(self.emb.databaseDirectory, dictionary_file_name))
            index_name = os.path.splitext(dictionary_file_name)[0]
            index_path = os.path.join(self.emb.indexDirectory, index_name)

            self.embe.index([{"table_name": command["table_name"],
                "table_description": command["table_description"],
                "field_name": command["field_name"],
                "field_type": command["field_type"],
                "field_references": command["field_references"],
                "field_description": command["field_description"],
                "text": command["field_description"]} for command in commands])                

            self.embe.save(index_path)
            print("index path", index_path)
            self.embe.close()

        except FileNotFoundError:
            print(f"File '{dictionary_file_name}' or its path not found.")
        except Exception as e:
            print(f"An error occurred in generareIndex in UploadServiceTemplace.py: {e}")