import os
import sys
import json
import shutil

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, "..")))

from schemaValidator import jsonValidator
from loadingUtils import loading_animation

database_path = os.path.join(dirPath, "..", "database")
JSON_schema = os.path.join(dirPath, "..", "JSON", "schema.json")

def getFiles():
    if not os.path.exists(database_path):
        return "Error: The database directory does not exist. Please check the path."

    files = os.listdir(database_path)

    if not files:
        return "There are no files in the database directory. Add a file first."

    filesList = "\n".join([f"- {file}" for file in files])
    loading_animation(0.25)
    return f"Files in the database directory:\n{filesList}"

def addFile():
    while True:
        input_path = input("Enter the full path to the file you want to upload (or type 'cancel' to go back): ").strip().strip("'\"")

        if input_path.lower() == "cancel":
            print("\033[1mUpload cancelled. You will be redirected to the admin menu.\033[0m")
            return

        if not os.path.isfile(input_path) or not input_path.endswith(".json"):
            print("Invalid file path or format. Please enter a valid path to a JSON file.")
            continue

        with open(JSON_schema, "r") as schema_file, open(input_path, "r") as data_file:
            json_schema, json_data = json.load(schema_file), json.load(data_file)

        # Check compliance
        is_compliant, error_message = jsonValidator(json_data, json_schema)

        if not is_compliant:
            print(f"The JSON is not compliant with the schema. Error: {error_message}")
            continue

        base_filename = os.path.basename(input_path)
        new_file_path = os.path.join(database_path, base_filename)

        if os.path.exists(new_file_path):
            print("File already exists in the database directory.")
        else:
            loading_animation(0.75)
            shutil.copyfile(input_path, new_file_path)
            print("File added to the database directory.")

def deleteFile():
    # Visualizzazione di tutti i file presenti nel database prima di consentire l'eliminazione
    print(getJsonFiles())
    
    filename_to_delete = input("Enter the filename you want to delete from the database: (file_name/exit): ")
    if filename_to_delete.lower() in ["exit", "e"]:
        return
    else:
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
                # Chiedi conferma prima di eliminare il file
                confirm = input(f"Are you sure you want to delete '{os.path.basename(file_path)}'? (yes/no): ").lower()
                if confirm.lower() in ["yes", "y"]:
                    # Elimina il file
                    loading_animation(1)
                    os.remove(file_path)
                    print(f"File '{os.path.basename(file_path)}' has been deleted.")
                    file_deleted = True
                    break
                elif confirm.lower() in ["no", "n"]:
                    print(f"Deletion of '{os.path.basename(file_path)}' canceled.")
                    file_deleted = True  # Consider the file as deleted to skip the "not file_deleted" message
                    break
                
        if not file_deleted:
            print(f"File '{filename_to_delete}' does not exist in the database directory.")
            deleteFile()
        
def getJsonFiles():
    if not os.path.exists(database_path):
        return "Error: The database directory does not exist. Please check the path."

    files = os.listdir(database_path)
    json_files = [file for file in files if file.endswith('.json')]

    if not json_files:
        return "There are no JSON files in the database directory. Add a JSON file first."

    filesList = "\n".join([f"- {file}" for file in json_files])
    loading_animation(0.25)
    return f"JSON files in the database directory:\n{filesList}"
