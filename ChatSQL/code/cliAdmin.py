import os
import shutil
import json
from schemaValidator import jsonValidator

#Global variables
dirPath = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(dirPath, "..", "database")

JSON_schema = os.path.join(dirPath, "..", "JSON", "schema.json")

def admin():
    print("\n\033[1mWelcome to the admin section 👨🏻‍💻\033[0m")
    while True:
        print("\nWhat do you want to do?")
        print("1. Add file")
        print("2. Delete file")
        print("3. Get files")
        print("4. Exit the admin section")
        choice = input("Your choice: ")
        if choice == "1" or choice == "add":
            addFile()
        elif choice == "2" or choice == "delete":
            deleteFile()
        elif choice == "3" or choice == "files":
            print(getFiles(database_path))
        elif choice == "4" or choice == "exit":
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
    inputFile = input("Enter the full path to the file you want to upload:")
    databaseFile = inputFile.strip().strip("'\"")

    # Check if the "database" directory exists, if not, create it
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    # Load JSON Schema from file
    with open(JSON_schema, "r") as schema_file:
        json_schema = json.load(schema_file)

    # Load JSON data from file
    with open(databaseFile, "r") as data_file:
        json_data = json.load(data_file)

    # Check compliance
    is_compliant = jsonValidator(json_data, json_schema)

    # Check if filename is already in the database and if it is a JSON file
    if os.path.isfile(databaseFile) and databaseFile.endswith(".json") and is_compliant:
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

    elif not is_compliant:
        print("The JSON is not compliant with the schema.")

    else:
        print("File does not exist or is not a JSON file.")


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