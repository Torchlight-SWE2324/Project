import os
import sys
import csv

def checkData(username, password):
    with open("pswrd.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True

def admin():
    print("ADMIN PAGE")
    username = input("username: ")
    password = input("password: ")
    # check if username and password are in the pswrd.csv
    if username == "admin" and password == "admin":
        print("username and password correct")
        while True:
            print("1. Add file")
            print("2. Delete file")
            print("3. Exit")
            choice = input("Your choice: ")
            if choice == "1" or choice == "add":
                addFile()
            elif choice == "2" or choice == "delete":
                deleteFile()
            elif choice == "3" or choice == "exit":
                print("Goodbye 👋")
                break
            else:
                print("Invalid choice")
    else:
        print("username or password incorrect")

def getFiels():
    # Specify the path to the "database" directory
    database_path = "/Users/giovannifilippini/Desktop/UNI/swe/progetto/1_repos/ChatSQL/ChatSQL/playground/database"

    # Check if the "database" directory exists, if not, create it
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    # Return the list of files in the "database" directory
    return os.listdir(database_path)

def addFile():
    # ask for filename with full path
    filename = input("Enter the full path to the file you want to upload: ")

    # Specify the path to the "database" directory
    database_path = "/Users/giovannifilippini/Desktop/UNI/swe/progetto/1_repos/ChatSQL/ChatSQL/playground/database"

    # Check if the "database" directory exists, if not, create it
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    # Check if filename is already in the database and if it is a JSON file
    if filename in os.listdir(database_path) and filename.endswith(".json"):
        print("file already exists")
    else:
        # Create the file using the full path to the file
        with open(os.path.join(database_path, filename), "w") as f:
            f.write("{}")
        print("file created")

def deleteFile():
    filename = input("Delete file: ")
    # check if filename is in the database and if the file is a JSON file
    if filename in os.listdir("database") and filename.endswith(".json"):
        # delete the file
        os.remove(f"database/{filename}")
        print("file deleted")
    else:
        print("file does not exist")