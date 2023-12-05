import os
import shutil

#Global variables
dirPath = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(dirPath, "database") 

def admin():
    print("\n\033[1mWelcome to the admin section 👨🏻‍💻\033[0m")
    while True:
        print("1. Add file")
        print("2. Delete file")
        print("3. Get files")
        print("4. Exit")
        choice = input("Your choice: ")
        if choice == "1" or choice == "add":
            addFile()
        elif choice == "2" or choice == "delete":
            deleteFile()
        elif choice == "3" or choice == "files":
            print(getFiels())
        elif choice == "4" or choice == "exit":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice")

def getFiels():
    if not os.path.exists(database_path):
        return "There are no files in the database directory. Add a file first."
    elif os.path.exists(database_path):
        return os.listdir(database_path)

def addFile():
    # Ask for filename with full path
    filename = input("Enter the full path to the file you want to upload:")

    # Check if the "database" directory exists, if not, create it
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    # Check if filename is already in the database and if it is a JSON file
    if os.path.isfile(filename) and filename.endswith(".json"):
        # Extract the filename from the full path
        base_filename = os.path.basename(filename)

        # Create the file path for the new file in the "database" directory
        new_file_path = os.path.join(database_path, base_filename)

        # Check if the file already exists in the database
        if os.path.exists(new_file_path):
            print("File already exists in the database directory.")
        else:
            # Copy the content of the original file to the new file in the "database" directory
            shutil.copyfile(filename, new_file_path)
            print("File copied to the database directory.")
    else:
        print("File does not exist or is not a JSON file.")

def deleteFile():
    # Take the filename to delete as user input
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