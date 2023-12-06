import os
import shutil
import json
import re

from schemaValidator import jsonValidator

#Global variables
dirPath = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(dirPath, "database")

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
    files = os.listdir(database_path)
    filesList = "\n".join([f"- {file}" for file in files])

    if not files:
        return "There are no files in the database directory. Add a file first."
    
    if not os.path.exists(database_path):
        return "Error: The database directory does not exist. Please check the path."
    
    return f"Files in the database directory:\n{filesList}"


def addFile():
    while True:
        inputFile = input("Enter the full path to the file you want to upload (or type 'cancel' to go back): ")
        
        if inputFile.lower() == "cancel":
            print("\033[1mUpload cancelled. You will be redirected to the admin menu.\033[0m")
            return

        databaseFile = inputFile.strip().strip("'\"")

        if not os.path.isfile(databaseFile):
            print("Invalid file path. Please enter a valid file path.")
            continue

        if not databaseFile.endswith(".json"):
            print("Invalid file format. Please enter a path to a JSON file.")
            continue

        # Load JSON Schema from file
        with open(JSON_schema, "r") as schema_file:
            json_schema = json.load(schema_file)

        # Load JSON data from file
        with open(databaseFile, "r") as data_file:
            json_data = json.load(data_file)

        # Check compliance
        is_compliant = jsonValidator(json_data, json_schema)

        if not is_compliant:
            print("The JSON is not compliant with the schema. Please choose a valid JSON file.")
            continue

        # Extract the filename from the full path
        base_filename = os.path.basename(databaseFile)

        # Create the file path for the new file in the "database" directory
        new_file_path = os.path.join(database_path, base_filename)

        # Check if the file already exists in the database
        if os.path.exists(new_file_path):
            print("File already exists in the database directory.")
        else:
            # Copy the content of the original file to the new file in the "database" directory
            shutil.copyfile(databaseFile, new_file_path)
            print("File copied to the database directory.")


def deleteFile():
    filename_to_delete = input("Enter the filename you want to delete from the database: ")

    # Create the full path to the file in the database directory
    file_path = os.path.join(database_path, filename_to_delete)

    # Check if the file exists before attempting to delete
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print(f"File '{filename_to_delete}' has been deleted.")
    else:
        print(f"File '{filename_to_delete}' does not exist in the database directory.")