import os
import json

from txtai import Embeddings

class Embedder:
    def __init__(self):
        self.emb = None
        self.indexDirectory = os.path.join(os.path.dirname(__file__), "indexes")
        self.databaseDirectory = os.path.join(os.path.dirname(__file__), "database")

    def generateIndex(self, dictionary_file_name):
        try:
            if not os.path.exists(self.indexDirectory):
                os.makedirs(self.indexDirectory)

            commands = self.generateUpsertCommands(os.path.join(self.databaseDirectory, dictionary_file_name))
            index_name = os.path.splitext(dictionary_file_name)[0]
            index_path = os.path.join(self.indexDirectory, index_name)

            self.getEmb().index([{"table_name": command["table_name"],
                              "table_description": command["table_description"],
                              "field_name": command["field_name"],
                              "field_type": command["field_type"],
                              "field_references": command["field_references"],
                              "field_description": command["field_description"],
                              "text": command["field_description"]} for command in commands])

            self.getEmb().save(index_path)
            self.getEmb().close()
            return "index_created"

        except FileNotFoundError:
            return f"File '{dictionary_file_name}' or its path not found."
        
        except Exception as e:
            return f"An error occurred in generateIndex in embedder.py: {e}"

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
            self.getEmb().load(index_path)
            
        except FileNotFoundError:
            print(f"Index file '{dictionary_file_name}' or its path not found.")
        
        except Exception as e:
            print(f"An error occurred in caricareIndex in : {e}")

    def save(self):
        self.getEmb().save(self.indexDirectory)

    def close(self):
        self.getEmb().close(self.indexDirectory)

    def getEmb(self):
        if self.emb == None:
            self.emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})
        return self.emb