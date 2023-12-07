import os
import sys
import csv
from cliAdmin import admin

dirPath = os.path.dirname(os.path.realpath(__file__))

def checkData(username, password):
    file_path = os.path.join(dirPath, "pswrd.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True

def adminAuth():
    username = input("Username: ")
    password = input("Password: ")
    if checkData(username, password):
        admin()
    else:
        print("username or password incorrect")

def main():
    print("\nWelcome to the ChatSQL CLI (\033[1mPLAYGROUND 🛝\033[0m)")
    while True:
        print("\nWhat do you want to do?")
        print("1. Admin")
        print("2. Ask")
        print("3. Exit the program")
        choice = input("Your choice: ")
        if choice == "1" or choice == "admin":
            adminAuth()
        elif choice == "2" or choice == "ask":
            pass
        elif choice == "3" or choice == "exit":
            confirmation = input("Are you sure you want to exit the program? (yes/no): ").lower()
            if confirmation == "yes":
                print("Exiting the program. Bye 👋🏻")
                sys.exit()
            elif confirmation == "no":
                print("Returning to the main menu.")
            else:
                print("Invalid choice. Returning to the main menu.")


if __name__ == "__main__":
    main()