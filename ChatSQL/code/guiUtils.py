#versione per GUI di utils.py

import os
import sys
import json

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

def generateEmbeddingUpsert(jsonFileName):
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