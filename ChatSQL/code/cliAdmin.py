import re

from fileOperations import getFiles, addFile, deleteFile

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
            print("Files in the database:" + getFiles())
        elif re.match(r"^4$|^exit$", choice):
            confirmation = input("Are you sure you want to exit the admin section? (yes/no): ").lower()
            if confirmation.lower() in ["yes", "y"]:
                print("Leaving admin section. You will be redirected to the main menu.")
                break
            elif confirmation.lower() in ["no", "n"]:
                print("Returning to the admin section menu.")
            else:
                print("Invalid choice. Returning to the admin section menu.")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    print("Files in the database:" + getFiles())