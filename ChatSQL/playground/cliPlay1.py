import os
import sys
import csv
from cliAdmin import admin

dirPath = os.path.dirname(os.path.realpath(__file__))
# print the current directory
print(dirPath)

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
    print("Welcome to the ChatSQL CLI (\033[1m PLAYGROUND 🛝 \033[0m)")
    while True:
        print("What do you want to do?")
        print("1. Admin")
        print("2. Ask")
        print("3. Exit")
        choice = input("Your choice: ")
        if choice == "1" or choice == "admin":
            adminAuth()
        elif choice == "2" or choice == "ask":
            pass
        elif choice == "3" or choice == "exit":
            print("Goodbye 👋")
            sys.exit()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()