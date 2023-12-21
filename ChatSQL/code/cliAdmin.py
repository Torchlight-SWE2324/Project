from fileOperations import getFiles, addFile, deleteFile

def admin():
    print("\n\033[1mWelcome to the admin section\033[0m")
    while True:
        print("\nWhat do you want to do?")
        print("1. Add a file")
        print("2. Delete a file")
        print("3. Get all the file sin the database")
        print("4. Leave the admin section")

        choice = input("Your choice: ").lower()

        if choice == "1" or choice == "add":
            addFile()
        elif choice == "2" or choice == "delete":
            deleteFile()
        elif choice == "3" or choice == "get":
            print("Files in the database:" + getFiles())
        elif choice == "4" or choice == "leave":
            handle_exit()
        else:
            print("Invalid choice")

def handle_exit():
    confirmation = input("Are you sure you want to leave the admin section? (yes/no): ").lower()
    if confirmation == "yes" or confirmation == "y":
        print("Leaving admin section. You will be redirected to the main menu.")
    elif confirmation == "no" or confirmation == "n":
        print("Returning to the admin section menu.")
    else:
        print("Invalid choice. Returning to the admin section menu.")


if __name__ == "__main__":
    print("Files in the database:" + getFiles())