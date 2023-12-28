# versione per GUI di fileOperations.py

import os
import sys
import json
import shutil
from guiUtils import jsonValidator

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, "..")))

database_path = os.path.join(dirPath, "..", "database")
JSON_schema = os.path.join(dirPath, "..", "code", "schema.json")

def getFiles(file_type='.json'):
    if not os.path.exists(database_path):
        return []
    files = os.listdir(database_path)
    filtered_files = [file for file in files if file.endswith(file_type)]
    if not filtered_files:
        return []
    return filtered_files

def deleteFile(filename_to_delete: str):
    # Aggiunta dell'estensione .json se l'utente non l'ha fornita
    if not filename_to_delete.endswith(".json"):
        filename_to_delete_with_extension = filename_to_delete + ".json"
        filename_to_delete_without_extension = filename_to_delete
    else:
        filename_to_delete_with_extension = filename_to_delete
        filename_to_delete_without_extension = filename_to_delete.replace(".json", "")

    # Tentativo di eliminare il file specificato con e senza estensione .json
    file_paths_to_try = [
        os.path.join(database_path, filename_to_delete_with_extension),
        os.path.join(database_path, filename_to_delete_without_extension)
    ]
    file_deleted = False
    for file_path in file_paths_to_try:
        if os.path.exists(file_path):
            # Elimina il file
            os.remove(file_path)
            file_deleted = True
            return f'File "{filename_to_delete}" deleted successfully'
    if not file_deleted:
        return f'Error: file "{filename_to_delete}" could not be deleted'

def uploadFile(file_content, file_name):
    if not file_name.endswith(".json"):
        return "Invalid format. Please enter a JSON file."
    
    file_content_str = file_content.decode('utf-8')
    try:
        with open(JSON_schema, "r") as schema_file:
            json_schema, json_data = json.load(schema_file), json.loads(file_content_str)
    except json.JSONDecodeError as e:
        return f"JSON file could not be loaded. Error: {e}"
    
    is_compliant, error_message = jsonValidator(json_data, json_schema)
    if not is_compliant:
        return f"JSON file is not compliant with the schema. Error: {error_message}"
    
    destination_path = os.path.join(database_path, file_name)
    with open(destination_path, "wb") as destination_file:
        destination_file.write(file_content)
    
    return f'File "{file_name}" uploaded!'
