import os
import json
from txtai import Embeddings


    # self.nome_dizionario_corrente = bar.json

    # Selezione nuovo corrente
    # - self.nome_dizionario_corrente = nome del dizionario appena salvato

    # salvare nuovo file
    #       - generazione index
    #       - salvare l'index
    #       - self.nome_dizionario_corrente = nome del dizionario appena salvato
    # dentro alla classe UploadService chiami 


""" dentro alla classe Modelupload      
        
        embedder = EmbedderFactory()
        embedder.getEmb().index()

        self.nome_dizionario_corrente = nome del dizionario appena salvato

        embedder.getEmb().save()
"""

    # eliminare dizionario
    #       - eliminare(index da eliminare è caricato dentro)
    #       - self.nome_dizionario_corrente = nome del dizionario appena salvato

    # generare prompt
    # emb.load(bar.json)
    # emb.search
    # (generare prompt(index corrente))
    # dictionary_file_name = nome del dizionario attualmente selezionato

    # generare debug
    # emb.load(load index corrente)
    # emb.search
    # (generare debug(index corrente))
    # - generare debug(index corrente)
    # dictionary_file_name = nome del dizionario attualmente selezionato


class Embedder:
    def __init__(self):
        self.emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})


    def generateUpsertCommands(self, dictionary_path):

        db_dictionary_path = f"{dictionary_path}"
        print("db_dictionary_path:" + f"{db_dictionary_path}")
        print("dictionary_path:" + f"{dictionary_path}")
        with open(db_dictionary_path, 'r') as file:
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

    #generate index and save it into the folder indexes
    def generareIndex(self, dictionary_file_name):
        #hande if the folder does not exist
        if not os.path.exists("indexes"):
            os.makedirs("indexes")
        # file directory: ./database/{dictionary_file_name}

        appen_path = f"Start/database/{dictionary_file_name}"
        commands = self.generateUpsertCommands(appen_path)
        self.emb.index(commands)
        self.emb.save(f"indexes/{os.path.splitext(dictionary_file_name)[0]}")

    def caricareIndex(self, dictionary_file_name):
        #hande if the folder does not exist
        self.emb.load(f"indexes/{os.path.splitext(dictionary_file_name)[0]}")

    def save(self):
        self.emb.save()

    def getEmb(self):
        return self.emb

    def setEmb(self, emb):
        self.emb = emb


if __name__ == "__main__":
    emb = Embedder()
    emb.generareIndex("swe_music.json")
    #emb.caricareIndex("auction.json")
