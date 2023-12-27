#versione per GUI di utils.py

import csv
import os
import sys
import json
from txtai import Embeddings

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

def upsert(commands):
    # Initialize the Embeddings module with the specified model
    #emb = Embeddings({"path": "sentence-transformers/stsb-roberta-large", "content": True})
    emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})

    # Upsert the data into the txtai Embeddings
    for command in commands:
        try:
            cmd = str(command)
            emb.upsert([cmd])
        except Exception as e:
            return f"Error during upsert: {e}"
    return emb

def generateUpsertCommands(jsonFileName):
    with open(jsonFileName, 'r') as file:
        data = json.load(file)

    commands = []
    index_counter = 0 # Contatore globale per il numero incrementale

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
            command = (index_counter, dictionary)
            commands.append(command)
            index_counter += 1
    return commands

def getPath(jsonFile):
    JSON_path = os.path.abspath(os.path.join(dirPath, os.pardir, "JSON"))
    # Construct the initial file path
    json_file_path = os.path.join(JSON_path, jsonFile)

    # Check if the file exists
    if not os.path.exists(json_file_path):
        # If the file doesn't exist, try adding the .json extension
        json_file_path = os.path.join(JSON_path, f"{jsonFile}.json")
        # Check again if the file exists
        if not os.path.exists(json_file_path):
            #return f"Error: The file '{jsonFile}' or '{jsonFile}.json' does not exist. Please check file name."
            return "Error"
    return json_file_path

def checkData(username, password):
    file_path = os.path.join(dirPath, "pswrd.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True