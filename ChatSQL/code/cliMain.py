from cliUser import user
from cliAdmin import admin
from utils import checkData, leaver

def main():
    print("\nWelcome to the ChatSQL CLI (\033[1mPLAYGROUND\033[0m)")
    while True:
        print("What do you want to do?")
        print("1. Access the admin section")
        print("2. Interact with the database")
        print("3. Exit the program")
        choice = input("Choose one of the options above (type the number or the name of the option): ").lower()
        if choice == "1" or choice == "admin":
            adminAuth()
        elif choice == "2" or choice == "interact":
            user()
        elif choice == "3" or choice == "exit":
            leave = leaver("program")
            if leave == True:
                break
            else:
                continue
        else:
            print("Invalid choice\n")

def adminAuth():
    username = input("Username: ")
    password = input("Password: ")
    if checkData(username, password):
        admin()
    else:
        print("username or password incorrect")

if __name__ == "__main__":
    main()