import os
import sys
import json
import shutil

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, "..")))

from utils import jsonValidator, loading_animation

database_path = os.path.join(dirPath, "..", "database")
JSON_schema = os.path.join(dirPath, "..", "code", "schema.json")

def getFiles(file_type='.json'):
    if not os.path.exists(database_path):
        return "Error: The database directory does not exist. Please check the path."

    files = os.listdir(database_path)
    filtered_files = [file for file in files if file.endswith(file_type)]

    if not filtered_files:
        return f"There are no {file_type.upper()} files in the database directory. Add a file first."

    filesList = "\n".join([f"- {file}" for file in filtered_files])
    loading_animation(0.25)
    return f"\n\nFiles in the database:\n{filesList}\n"

def uploadFile():
    while True:
        input_path = input("Enter the full path to the file you want to upload (or type 'exit' to go back): ").strip().strip("'\"").lower()

        if input_path == "exit" or input_path == "e":
            print("\033[1mUpload cancelled. You will be redirected to the admin menu.\033[0m")
            return

        if not os.path.isfile(input_path) or not input_path.endswith(".json"):
            print("Invalid file path or format. Please enter a valid path to a JSON_old_versions file.")
            continue

        with open(JSON_schema, "r") as schema_file, open(input_path, "r") as data_file:
            json_schema, json_data = json.load(schema_file), json.load(data_file)

        # Check compliance
        is_compliant, error_message = jsonValidator(json_data, json_schema)

        if not is_compliant:
            print(f"The JSON_old_versions is not compliant with the schema. Error: {error_message}")
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
    # View all the files in the database
    print(getFiles())
    
    filename_to_delete = input("Enter the name of the file you want to delete (or type 'exit' to go back): ").strip().strip("'\"").lower()
    if filename_to_delete == "exit" or filename_to_delete == "e":
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
                confirm = input(f"Are you sure you want to delete the file \033[1m'{os.path.basename(file_path)}'\033[0m? (yes/no): ").lower()
                if confirm.lower() in ["yes", "y"]:
                    # Elimina il file
                    loading_animation(1)
                    os.remove(file_path)
                    print(f"The file \033[1m'{os.path.basename(file_path)}'\033[0m has been deleted.")
                    file_deleted = True
                    break
                elif confirm.lower() in ["no", "n"]:
                    print(f"Deletion of the file \033[1m'{os.path.basename(file_path)}'\033[0m has been cancelled.")
                    file_deleted = True  # Consider the file as deleted to skip the "not file_deleted" message
                    break
                
        if not file_deleted:
            print(f"The file \033[1m'{filename_to_delete}'\033[0m does not exist in the database directory.")
            deleteFile()