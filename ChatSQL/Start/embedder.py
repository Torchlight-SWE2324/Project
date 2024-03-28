import os
import json
from txtai import Embeddings

class Embedder:
    def __init__(self, model_path, data_path):
        self.emb = Embeddings({"path": model_path, "content": True})
        self.data_path = data_path
        self.indexDirectory = os.path.join(os.path.dirname(__file__), "indexes")
        self.databaseDirectory = os.path.join(os.path.dirname(__file__), "database")

    def generateUpsertCommands(self, dictionary_path):
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

    def generareIndex(self, dictionary_file_name):
        if not os.path.exists(self.indexDirectory):
            os.makedirs(self.indexDirectory)
        
        commands = self.generateUpsertCommands(os.path.join(self.databaseDirectory, dictionary_file_name))

        print("index directory",self.indexDirectory)
        print("database directory",self.databaseDirectory)
        print("name dictionary",dictionary_file_name)
        print("join",os.path.join(self.databaseDirectory, dictionary_file_name))
        
        index_name = os.path.splitext(dictionary_file_name)[0]
        index_path = os.path.join(self.indexDirectory, index_name)

        for command in commands:
            self.emb.index(command)

        self.emb.save(index_path)

        self.emb.close()

    def caricareIndex(self, dictionary_file_name):
        index_name = os.path.splitext(dictionary_file_name)[0]
        index_path = os.path.join(self.indexDirectory, index_name)
        
        self.emb.load(index_path)

    def save(self):
        self.emb.save()

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