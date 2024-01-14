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


def upsert(commands):
    emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})

    emb.index([{"table_name": command["table_name"], "table_description": command["table_description"],
                "field_name": command["field_name"], "field_type": command["field_type"], "field_references": command["field_references"],
                "text": command["table_description"]} for command in commands])
    return emb


def getDictionariesFolderPath():
    utils_folder_path = os.path.dirname(os.path.realpath(__file__))
    dictionaries_folder_path = os.path.abspath(os.path.join(utils_folder_path, "database"))
    return dictionaries_folder_path


def checkData(username, password):
    file_path = os.path.join(dirPath, "pswrd.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True