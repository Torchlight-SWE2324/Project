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
    emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})

    emb.index([{"table_name": command["table_name"], "table_description": command["table_description"], # ?? DA CAMBIARE PER UPSERT
                "field_name": command["field_name"], "field_type": command["field_type"], "field_references": command["field_references"],
                "text": command["field_description"]} for command in commands])

    return emb

def generateUpsertCommands(dictionary_path):
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

def getDictionaryPath(dictionary_file_name):
    dictionaries_folder_path = os.path.abspath(os.path.join(dirPath, "database"))
    # Construct the initial file path
    dictionary_file_path = os.path.join(dictionaries_folder_path, dictionary_file_name)

    # Check if the file exists
    if not os.path.exists(dictionary_file_path):
        # If the file doesn't exist, try adding the .json extension
        dictionary_file_path = os.path.join(dictionaries_folder_path, f"{dictionary_file_name}.json")
        # Check again if the file exists
        if not os.path.exists(dictionary_file_path):
            #return f"Error: The file '{dictionary_file_name}' or '{dictionary_file_name}.json' does not exist. Please check file name."
            return "Error"
    return dictionary_file_path

def checkData(username, password):
    file_path = os.path.join(dirPath, "pswrd.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True