import os
import sys
import csv
import time
import json
from jsonschema import validate, ValidationError

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

database_path = os.path.join(dirPath, "..", "database")
JSON_schema = os.path.join(dirPath, "..", "JSON", "schema.json")

def checkData(username, password):
    file_path = os.path.join(dirPath, "pswrd.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password and row[2] == "admin":
                return True

def leaver(section):
    confirmation = input(f"Are you sure you want to leave the {section} section? (y/n): ").lower()
    if confirmation == "yes" or confirmation == "y":
        print(f"Leaving the {section}. Bye!\n")
        return True
    elif confirmation == "no" or confirmation == "n":
        print(f"Returning to the {section} section.\n")
        return False
    else:
        print(f"Invalid choice. Returning to the {section} menu.\n")
        return False

def loading_animation(n):
    animation_chars = "|/-\\"
    start_time = time.time()

    while time.time() - start_time < n:
        for char in animation_chars:
            sys.stdout.write("\r" + "Loading " + char)
            sys.stdout.flush()
            time.sleep(0.1)

    sys.stdout.write("\r")  # Move cursor to the beginning of the line


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
            dictionary = {"table": table_name,"table-description": table_description,"field": field_name, "type": type, "references": references, "description": description}
            command = (index_counter, dictionary)

            commands.append(command)

            index_counter += 1
    return commands

def jsonValidator(json_data, json_schema):
    try:
        validate(instance=json_data, schema=json_schema)
        return True, None
    except ValidationError as e:
        return False, str(e)