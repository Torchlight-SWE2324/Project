import json

from txtai import Embeddings


class EmbeddingsHandler:
    def __init__(self, dictionary_path, commands) -> None:
        self.dictionary_path = dictionary_path
        self.commands = commands

    #generateUpsertCommands
    # Dato un file JSON, restituisce una lista di comandi upsert per l'indice txtai
    def index(self, dictionary_path):
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

                # Create the emb.upsert command
                dictionary = {"table_name": table_name, "table_description": table_description, "field_name": field_name,
                            "field_type": type, "field_references": references, "field_description": description}
                commands.append(dictionary)
        return commands
    
    #upsert
    # Dato un insieme di comandi upsert, crea un indice txtai e lo restituisce
    def load(self, commands):
        emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})
        emb.index([{"table_name": command["table_name"], "table_description": command["table_description"], "field_name": command["field_name"], "field_type": command["field_type"], "field_references": command["field_references"], "text": command["table_description"]} for command in commands])
        return emb



if __name__ == "__main__":
    path = "C:/Users/Marco/Desktop/swe/progetto/ChatSQL/ChatSQL/JSON/auction.json"
    handler = EmbeddingsHandler(dictionary_path=path, commands=None)
    print(handler.index(path))
    