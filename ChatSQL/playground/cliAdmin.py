from fileOperations import getFiles, uploadFile, deleteFile
from utils import leaver

def admin():
    print("\n\033[1mWelcome to the admin section\033[0m")
    while True:
        print("What do you want to do?")
        print("1. Add a file")
        print("2. Delete a file")
        print("3. Get all the files in the database")
        print("4. Leave the admin section")
        print("Type the number of the option you want to choose or type the name of the option (e.g. 'add', 'delete', 'get', 'leave')")

        choice = input("Your choice: ").lower()

        if choice == "1" or choice == "add":
            uploadFile()
        elif choice == "2" or choice == "delete":
            deleteFile()
        elif choice == "3" or choice == "get":
            print("Files in the database:" + getFiles())
        elif choice == "4" or choice == "leave":
            leave = leaver("admin")
            if leave == True:
                break
            else:
                continue
        else:
            print("Invalid choice\n")

if __name__ == "__main__":
    admin()