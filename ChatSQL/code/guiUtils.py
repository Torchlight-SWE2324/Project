#versione per GUI di utils.py

import csv
import os
import sys
import json
from txtai import Embeddings
from jsonschema import validate, ValidationError


dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

def jsonValidator(json_data, json_schema):
    try:
        validate(instance=json_data, schema=json_schema)
        return True, None
    except ValidationError as e:
        return False, str(e)

def upsert(commands): #???? è QUI DA FARE SALVATAGGIO INDICE??
    # Initialize the Embeddings module with the specified model
    #emb = Embeddings({"path": "sentence-transformers/stsb-roberta-large", "content": True})
    emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})

    # Upsert the data into the txtai Embeddings
    for command in commands:
        try:
            cmd = str(command) #""""""""""""""""""""""""""""""""""""""""""
            emb.upsert([cmd])
        except Exception as e:
            return f"Error during upsert: {e}" #??? DA IMPLEMENTARE CATCH INTORNO FUNZIONE
    return emb

def generateUpsertCommands(jsonFilePath):
    with open(jsonFilePath, 'r') as file:
        data = json.load(file)

    commands = []
    index_counter = 0 #?????? SERVE # Contatore globale per il numero incrementale

    for table in data["tables"]:
        table_name = table["name"]
        table_description = table["table-description"]

        for column in table["columns"]:
            field_name = column["name"]
            type = column["type"]
            references = column["references"]
            description = column["description"]

            # Create the emb.upsert command
            dictionary = {"table": table_name, "table-description": table_description, "field": field_name,
                          "type": type, "references": references, "description": description}
            command = (index_counter, dictionary) #!!!!!!!!!!!!!!!!! DA RIDEFINIRE
            commands.append(command)
            index_counter += 1
    return commands

def getPath(dictionaryFileName):
    dictionariesFolderPath = os.path.abspath(os.path.join(dirPath, "database"))
    # Construct the initial file path
    dictionaryFilePath = os.path.join(dictionariesFolderPath, dictionaryFileName)

    # Check if the file exists
    if not os.path.exists(dictionaryFilePath):
        # If the file doesn't exist, try adding the .json extension
        dictionaryFilePath = os.path.join(dictionariesFolderPath, f"{dictionaryFileName}.json")
        # Check again if the file exists
        if not os.path.exists(dictionaryFilePath):
            #return f"Error: The file '{dictionaryFileName}' or '{dictionaryFileName}.json' does not exist. Please check file name."
            return "Error"
    return dictionaryFilePath

def checkData(username, password):
    file_path = os.path.join(dirPath, "pswrd.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True