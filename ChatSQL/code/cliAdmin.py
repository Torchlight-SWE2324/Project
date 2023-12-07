import os
import sys
import shutil
import json
import re

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

from schemaValidator import jsonValidator
from playground.loading import loading_animation

database_path = os.path.join(dirPath, "..", "database")
JSON_schema = os.path.join(dirPath, "..", "JSON", "schema.json")

def admin():
    print("\n\033[1mWelcome to the admin section\033[0m")
    while True:
        print("\nWhat do you want to do?")
        print("1. Add file")
        print("2. Delete file")
        print("3. Get files")
        print("4. Leave the admin section")

        choice = input("Your choice: ").lower()

        if re.match(r"^1$|^add$", choice):
            addFile()
        elif re.match(r"^2$|^delete$", choice):
            deleteFile()
        elif re.match(r"^3$|^get$", choice):
            print(getFiles(database_path))
        elif re.match(r"^4$|^exit$", choice):
            print("Leaving admin section. You will be redirected to the main menu.")
            break
        else:
            print("Invalid choice")

def getFiles(database_path):
    if not os.path.exists(database_path):
        return "Error: The database directory does not exist. Please check the path."

    files = os.listdir(database_path)

    if not files:
        return "There are no files in the database directory. Add a file first."

    filesList = "\n".join([f"- {file}" for file in files])
    loading_animation(.25)
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
        is_compliant = jsonValidator(json_data, json_schema)

        if not is_compliant:
            print("The JSON is not compliant with the schema. Please choose a valid JSON file.")
            continue

        base_filename = os.path.basename(input_path)
        new_file_path = os.path.join(database_path, base_filename)

        if os.path.exists(new_file_path):
            print("File already exists in the database directory.")
        else:
            shutil.copyfile(input_path, new_file_path)
            loading_animation(1.25)
            print("File copied to the database directory.")

def deleteFile():
    filename_to_delete = input("Enter the filename you want to delete from the database: ")
    file_path = os.path.join(database_path, filename_to_delete)

    if os.path.exists(file_path):
        os.remove(file_path)
        loading_animation(.75)
        print(f"File '{filename_to_delete}' has been deleted.")
    else:
        print(f"File '{filename_to_delete}' does not exist in the database directory.")