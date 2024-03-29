import os
import json
from txtai import Embeddings

class Embedder:
    def __init__(self):
        self.emb= Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})
        self.indexDirectory = os.path.join(os.path.dirname(__file__), "indexes")
        self.databaseDirectory = os.path.join(os.path.dirname(__file__), "database")

    def generateUpsertCommands(self, dictionary_path):
        try:
            with open(dictionary_path, 'r') as file:
                data = json.load(file)
            commands = []
            

            for table in data["tables"]:
                table_name = table["name"]
                table_description = table["table-description"]

                for column in table["columns"]:
                    field_name = column["name"]
                    type = column["type"]
                    references = column["references"]
                    description = column["description"]

                    dictionary = {"table_name": table_name,
                                "table_description": table_description,
                                "field_name": field_name,
                                "field_type": type, "field_references": references,
                                "field_description": description}

                    commands.append(dictionary)

            return commands
        
        except FileNotFoundError:
            print(f"File '{dictionary_path}' not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file '{dictionary_path}'.")
            return []

    def caricareIndex(self, dictionary_file_name):
        try:
            index_name = os.path.splitext(dictionary_file_name)[0]
            index_path = os.path.join(self.indexDirectory, index_name)

            self.emb.load(index_path)
            
        except FileNotFoundError:
            print(f"Index file '{dictionary_file_name}' or its path not found.")
        except Exception as e:
            print(f"An error occurred in caricareIndex in : {e}")

    def save(self):
        self.emb.save(self.indexDirectory)

    def getEmb(self):
        return self.emb

    def setEmb(self, emb):
        self.emb = emb





        
'''
if __name__ == "__main__":
    model_path = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    data_path = os.path.join(os.path.dirname(__file__), "indexes")

    emb = Embedder(model_path, data_path)
    #emb.generareIndex("swe_music.json")
    #pass the path indexes/swe_music/embeddings
    emb.caricareIndex(data_path + "/swe_music")
'''    
'''
    def generareIndex(self, dictionary_file_name):
        try:
            if not os.path.exists(self.indexDirectory):
                os.makedirs(self.indexDirectory)
            
            commands = self.generateUpsertCommands(os.path.join(self.databaseDirectory, dictionary_file_name))
            
            index_name = os.path.splitext(dictionary_file_name)[0]
            index_path = os.path.join(self.indexDirectory, index_name)

            for command in commands:
                self.emb.index(command)

            self.emb.save(index_path)

            self.emb.close()

        except FileNotFoundError:
            print(f"File '{dictionary_file_name}' or its path not found.")
        except Exception as e:
            print(f"An error occurred in generareIndex in Embedder.py: {e}")
'''